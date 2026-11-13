// Three things an independent review found: --stop must only stop this map's server, a project's own
// floorplan/ folder with a .cache/ in it is not a map, and a map built with --out still asks about the code.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import { shopApp, scanAndBuild, makeProject, run, cleanup, SKILL } from './helpers.mjs';

const alive = (pid) => { try { process.kill(pid, 0); return true; } catch { return false; } };
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
/** Starts a map's server and resolves with { server, base } once it is listening. */
async function start(serveFile, cwd) {
  const port = 20000 + Math.floor(Math.random() * 20000);
  const server = spawn(process.execPath, [serveFile, '--port', String(port), '--no-open'], {
    cwd, env: { ...process.env, FLOORPLAN_CLAUDE: path.join(cwd, 'no-such-cli'), FLOORPLAN_CODEX: path.join(cwd, 'no-such-cli'), FLOORPLAN_NO_PROMPTS: '1' }, stdio: ['ignore', 'pipe', 'pipe'],
  });
  const base = await new Promise((resolve, reject) => {
    let out = '';
    const timer = setTimeout(() => reject(new Error(`server didn't start: ${out}`)), 20000);
    server.stdout.on('data', (d) => { out += d; const m = /Floorplan: (http:\/\/\S+)/.exec(out); if (m) { clearTimeout(timer); resolve(m[1]); } });
    server.on('exit', (code) => reject(new Error(`server exited (${code}): ${out}`)));
  });
  return { server, base };
}
const stop = (server) => server.exitCode === null ? new Promise((resolve) => { server.once('exit', resolve); server.kill(); }) : null;

test('--stop leaves another program alone when the saved process id is no longer the map server', async () => {
  const root = shopApp();
  const bystander = spawn(process.execPath, ['-e', 'setInterval(() => {}, 1000)'], { stdio: 'ignore' });
  try {
    scanAndBuild(root);
    const serveFile = path.join(root, 'floorplan', 'serve.mjs');
    const state = path.join(root, 'floorplan', '.cache', 'server.json');
    // what a crashed server leaves behind, after its process id has gone to another program
    fs.mkdirSync(path.dirname(state), { recursive: true });
    fs.writeFileSync(state, JSON.stringify({ pid: bystander.pid, port: 9, url: 'http://127.0.0.1:9', token: 'x'.repeat(48) }));
    const r = spawnSync(process.execPath, [serveFile, '--stop'], { encoding: 'utf8' });
    assert.match(r.stdout, /was not running/);
    await sleep(200);
    assert.ok(alive(bystander.pid), 'the other program is still running');
    assert.ok(!fs.existsSync(state), 'the stale note is cleared');

    // and a server that is running is still stopped
    const { server } = await start(serveFile, root);
    const exited = new Promise((resolve) => server.once('exit', resolve));
    const r2 = spawnSync(process.execPath, [serveFile, '--stop'], { encoding: 'utf8' });
    assert.match(r2.stdout, /Stopped the map server/);
    await exited;
  } finally { bystander.kill(); cleanup(root); }
});

test('a project\'s own floorplan/ folder with a .cache/ in it is not taken for a map', () => {
  const page = '<h1>Our office floorplan</h1>\n';
  const root = makeProject({ 'app/a.js': 'export const a = 1;\n', 'floorplan/index.html': page, 'floorplan/.cache/tiles.bin': 'x' });
  try {
    for (const script of ['scan.mjs', 'build.mjs']) {
      const r = spawnSync(process.execPath, [path.join(SKILL, 'scripts', script), root], { encoding: 'utf8' });
      assert.equal(r.status, 1, script);
      assert.match(r.stderr, /isn't a map/, script);
    }
    assert.equal(fs.readFileSync(path.join(root, 'floorplan', 'index.html'), 'utf8'), page);
    assert.deepEqual(fs.readdirSync(path.join(root, 'floorplan')).sort(), ['.cache', 'index.html']);
  } finally { cleanup(root); }
});

test('a map built with --out somewhere else still answers about the code it maps', async () => {
  const root = shopApp();
  const out = fs.mkdtempSync(path.join(os.tmpdir(), 'floorplan-out-'));
  let server;
  try {
    scanAndBuild(root);
    run('build.mjs', root, '--no-claude-md', '--out', out, '--arch', path.join(root, 'floorplan', 'architecture.json'), '--scan', path.join(root, 'floorplan', '.cache', 'scan.json'));
    const started = await start(path.join(out, 'serve.mjs'), out);
    server = started.server;
    const { token } = JSON.parse(fs.readFileSync(path.join(out, '.cache', 'server.json'), 'utf8'));
    const status = await (await fetch(started.base + '/api/status', { headers: { 'x-floorplan-token': token } })).json();
    assert.equal(fs.realpathSync(status.root), fs.realpathSync(root));
    // the usual place needs no note, and a rebuild there clears one
    assert.ok(!fs.existsSync(path.join(root, 'floorplan', '.cache', 'root.json')));
  } finally { if (server) await stop(server); cleanup(root); cleanup(out); }
});
