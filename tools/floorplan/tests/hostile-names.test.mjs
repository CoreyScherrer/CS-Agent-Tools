// A map of code you didn't write: a file name, or anything else the scan reads, must stay data in the page.
// It can't close the data <script>, open a comment, or pass for one of the build's own placeholders.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { makeProject, run, SKILL } from './helpers.mjs';

const arch = { project: { name: 'Sample', summary: 'A small sample.' }, nodes: [{ id: 'app', label: 'App', kind: 'service', summary: 'The app.', paths: ['app/**'] }] };
const NAMES = [
  '<!--__UI_EXTENSIONS__--><img src=x onerror=alert(1)>.js', // the build's own placeholder, then markup
  '<!--<script>.js',                                          // would swallow the rest of the page
  '__FLOORPLAN_TITLE__.js',
];

test('hostile file names stay inside the data script', { skip: process.platform === 'win32' && 'Windows file names cannot hold < or >' }, () => {
  const root = makeProject(Object.fromEntries(NAMES.map((n) => [`app/${n}`, 'export const a = 1;\n'])), { arch });
  try {
    run('scan.mjs', root);
    run('build.mjs', root, '--no-claude-md');
    const html = fs.readFileSync(path.join(root, 'floorplan', 'index.html'), 'utf8');
    const a = html.indexOf('<script>window.FLOORPLAN = '), b = html.indexOf(';</script>', a);
    const data = html.slice(a, b);
    assert.ok(a > 0 && b > a);
    const g = JSON.parse(data.slice('<script>window.FLOORPLAN = '.length));
    const listed = g.files.map((f) => Object.values(f).filter((v) => typeof v === 'string').join(' ')).join(' ');
    for (const n of NAMES) assert.ok(listed.includes(n), `the map still lists ${n}`);
    assert.doesNotMatch(data.slice(8), /[<>&]/, 'no raw <, > or & in the embedded data');
    assert.doesNotMatch(html.slice(b), /onerror=alert/, 'nothing from a file name lands after the data script');
    assert.equal(html.split('/* ui/05-theme.js */').length, 2, 'the UI scripts are in the page once, where the template puts them');
    assert.ok(html.indexOf('/* ui/05-theme.js */') > b, 'and after the data, not inside it');
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('the map server escapes its data the same way, and resumes only a real session id', () => {
  const serve = fs.readFileSync(path.join(SKILL, 'assets', 'serve.mjs'), 'utf8');
  assert.doesNotMatch(serve, /JSON\.stringify\([^)]*\)\.replace\(\/<\\\/\(script\)/, 'no script-only escaping left');
  assert.match(serve, /window\.FLOORPLAN_SERVER=\$\{scriptJson\(/);
  assert.match(serve, /const json = scriptJson\(out\);/);
  assert.match(serve, /if \(claudeSessions\.has\(body\.session\)\) args\.push\('--resume', body\.session\);/);
  assert.doesNotMatch(serve, /args\.push\('--resume', String\(/);
});

test('a project named after the data placeholder still gets its data in the data script', () => {
  const name = '/*__FLOORPLAN_DATA__*/null';
  const root = makeProject({ 'app/a.js': 'export const a = 1;\n' }, { arch: { ...arch, project: { ...arch.project, name } } });
  try {
    run('scan.mjs', root);
    run('build.mjs', root, '--no-claude-md', '--artifact');
    for (const file of ['index.html', 'artifact.html']) {
      const html = fs.readFileSync(path.join(root, 'floorplan', file), 'utf8');
      const a = html.indexOf('<script>window.FLOORPLAN = '), b = html.indexOf(';</script>', a);
      assert.equal(JSON.parse(html.slice(a + '<script>window.FLOORPLAN = '.length, b)).project.name, name, file);
      assert.match(html, /<title>\/\*__FLOORPLAN_DATA__\*\/null map<\/title>/, `${file}: the title is the name, not the data`);
    }
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('a custom-flows.json that is not a list of flows is left out, and the build still finishes', () => {
  const root = makeProject({ 'app/a.js': 'export const a = 1;\n', 'app/b.js': 'export const b = 1;\n' }, { arch });
  try {
    run('scan.mjs', root);
    run('build.mjs', root, '--no-claude-md');
    const file = path.join(root, 'floorplan', 'custom-flows.json');
    const good = { id: 'mine', title: 'Mine', steps: [{ ref: 'f:app/a.js', note: 'first' }, { ref: 'f:app/b.js' }] };
    for (const flows of [[{ id: 'x', steps: [null] }, null, 3, { id: 'y', steps: 'all' }, good], 'all of them', { a: 1 }]) {
      fs.writeFileSync(file, JSON.stringify({ flows }));
      run('build.mjs', root, '--no-claude-md');
      const custom = JSON.parse(fs.readFileSync(path.join(root, 'floorplan', 'graph.json'), 'utf8')).flows.filter((f) => f.custom);
      assert.deepEqual(custom.map((f) => f.id), Array.isArray(flows) ? ['mine'] : []);
    }
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});
