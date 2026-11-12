// Fixes made in the CS-Agent-Tools bundle after its pre-release review. Each was reproduced first.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { makeProject, run, readGraph, cleanup, lib, SKILL, routeKeys, openEndpoints } from './helpers.mjs';

const arch = { project: { name: 'Sample', summary: 'A small sample.' }, nodes: [{ id: 'backend', label: 'Backend', kind: 'service', summary: 'The server.', paths: ['backend/**'] }] };
const FAKE_KEY = ['sk', 'live', 'a1B2c3D4e5F6g7H8i9J0k1L2m3N4'].join('_'); // made up, and never written whole in this file

test('a .env committed in a single-repo project is reported as committed, with the steps to untrack it', () => {
  const root = makeProject({ 'backend/.env': `STRIPE_SECRET_KEY=${FAKE_KEY}\n`, 'backend/server.js': 'export const a = 1;\n' }, { arch });
  try {
    const git = (...a) => execFileSync('git', ['-c', 'user.name=t', '-c', 'user.email=t@example.com', ...a], { cwd: root, stdio: 'pipe' });
    git('init', '-q'); git('add', '-f', 'backend'); git('commit', '-q', '-m', 'first');
    run('scan.mjs', root);
    run('build.mjs', root, '--no-claude-md');
    const health = JSON.stringify(readGraph(root).health);
    assert.match(health, /git rm --cached \\"backend\/\.env\\"/, 'the fix names the whole path and untracks it');
    assert.doesNotMatch(health, /[^a-z]ckend\/\.env/, 'no path with its start cut off');
  } finally { cleanup(root); }
});

test('a .gitignore that is not Floorplan\'s is left as it is', async () => {
  const { keepOutOfGit } = await lib('common.mjs');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'floorplan-gi-'));
  try {
    fs.writeFileSync(path.join(dir, '.gitignore'), '_build/\n*.tmp\n');
    assert.match(keepOutOfGit(dir), /has its own \.gitignore/);
    assert.equal(fs.readFileSync(path.join(dir, '.gitignore'), 'utf8'), '_build/\n*.tmp\n');
    const fresh = path.join(dir, 'map');
    assert.equal(keepOutOfGit(fresh), null);
    assert.match(fs.readFileSync(path.join(fresh, '.gitignore'), 'utf8'), /^# Floorplan[^\n]*\n\*\n$/);
  } finally { cleanup(dir); }
});

test('a sign-in check in front of an inline require() is seen, so the endpoints behind it are not reported as open', () => {
  const root = makeProject({
    'backend/app.js': "const express = require('express');\nconst { requireStaff } = require('./auth');\nconst app = express();\napp.use('/admin', requireStaff, require('./routes/admin'));\napp.listen(3000);\n",
    'backend/auth.js': "exports.requireStaff = function requireStaff(req, res, next) { if (!req.user || !req.user.staff) return res.status(403).end(); next(); };\n",
    'backend/routes/admin.js': "const router = require('express').Router();\nrouter.post('/users', (req, res) => { res.json({ ok: true }); });\nmodule.exports = router;\n",
  }, { arch });
  try {
    run('scan.mjs', root);
    run('build.mjs', root, '--no-claude-md');
    const graph = readGraph(root);
    assert.ok(routeKeys(graph).includes('POST /admin/users'), 'the endpoint is found under its mount');
    assert.deepEqual(openEndpoints(graph).filter((k) => /admin/.test(JSON.stringify(k))), []);
  } finally { cleanup(root); }
});

test('the map server takes any JSON body and never serves its cache folder', () => {
  const serve = fs.readFileSync(path.join(SKILL, 'assets', 'serve.mjs'), 'utf8');
  assert.doesNotMatch(serve, /body = JSON\.parse\(raw\)/, 'every body goes through parseBody');
  assert.equal(serve.split('const body = parseBody(raw);').length - 1, 5);
  assert.match(serve, /file\.startsWith\(path\.join\(here, '\.cache'\) \+ path\.sep\)/);
});
