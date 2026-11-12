// The map's local server: it listens only on this machine, and its API answers only the map page it
// served (a per-start token, from the same origin), so other websites can't use it.
import { test, before, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { shopApp, scanAndBuild, cleanup, mapLink } from './helpers.mjs';

let root, server, base, token;
before(async () => {
  root = shopApp();
  scanAndBuild(root);
  const port = 20000 + Math.floor(Math.random() * 20000);
  // no Claude Code or Codex CLI and no waitlist card: this only exercises the server itself
  server = spawn(process.execPath, [path.join(root, 'floorplan', 'serve.mjs'), '--port', String(port), '--no-open'], {
    cwd: root, env: { ...process.env, FLOORPLAN_CLAUDE: path.join(root, 'no-such-cli'), FLOORPLAN_CODEX: path.join(root, 'no-such-cli'), FLOORPLAN_NO_PROMPTS: '1' }, stdio: ['ignore', 'pipe', 'pipe'],
  });
  base = await new Promise((resolve, reject) => {
    let out = '';
    const timer = setTimeout(() => reject(new Error(`server didn't start: ${out}`)), 20000);
    server.stdout.on('data', (d) => { out += d; const m = /Floorplan: (http:\/\/\S+)/.exec(out); if (m) { clearTimeout(timer); resolve(m[1]); } });
    server.on('exit', (code) => reject(new Error(`server exited (${code}): ${out}`)));
  });
  token = /"token":"([0-9a-f]+)"/.exec(await (await fetch(mapLink(root))).text())?.[1];
});
after(async () => {
  // wait for the server to exit first: on Windows its working folder can't be removed while it runs
  if (server && server.exitCode === null) await new Promise((resolve) => { server.once('exit', resolve); server.kill(); });
  cleanup(root);
});

/** The cookie a browser holds once it has opened the map through its own link. */
const opened = () => ({ cookie: `fp_${new URL(base).port}=${new URL(mapLink(root)).searchParams.get('k')}` });
const api = (p, { headers = {}, ...opts } = {}) => fetch(base + p, { ...opts, headers: { 'content-type': 'application/json', ...headers } });

test('it listens on 127.0.0.1 only', () => {
  assert.match(base, /^http:\/\/127\.0\.0\.1:\d+$/);
});

test('the page it serves carries a fresh token', () => {
  assert.match(token || '', /^[0-9a-f]{32}$/);
});

test('API calls without the token are refused', async () => {
  assert.equal((await api('/api/flows')).status, 403);
  assert.equal((await api('/api/ask', { method: 'POST', body: '{"question":"hi"}' })).status, 403);
  assert.equal((await api('/api/flows', { headers: { 'x-floorplan-token': 'wrong' } })).status, 403);
});

test('API calls with the token from another website are refused', async () => {
  const r = await api('/api/flows', { headers: { 'x-floorplan-token': token, origin: 'https://evil.example' } });
  assert.equal(r.status, 403);
});

/** A request to the server under another host name, as a site that rebinds its domain to 127.0.0.1 would send. */
const asHost = (host, p) => new Promise((resolve, reject) => {
  const u = new URL(base + p);
  http.get({ hostname: u.hostname, port: u.port, path: u.pathname, headers: { host, 'x-floorplan-token': token, ...opened() } }, (r) => { r.resume(); resolve(r.statusCode); }).on('error', reject);
});

test('requests under any other host name are refused, page included (DNS rebinding)', async () => {
  const port = new URL(base).port;
  assert.equal(await asHost(`evil.example:${port}`, '/'), 403);
  assert.equal(await asHost(`evil.example:${port}`, '/api/flows'), 403);
  assert.equal(await asHost('127.0.0.1:1', '/'), 403);
  assert.equal(await asHost(`localhost:${port}`, '/'), 200);
  assert.equal(await asHost(`127.0.0.1:${port}`, '/api/flows'), 200);
});

test('the map and its files go only to a browser that came through the map\'s own link', async () => {
  const link = mapLink(root);
  const key = new URL(link).searchParams.get('k');
  assert.match(key, /^[0-9a-f]{32}$/);
  // the bare address, as any other account on this computer could ask for it: no page, so no token
  for (const p of ['/', '/index.html', '/graph.json', '/serve.mjs', '/?k=wrong', '/?k=']) {
    const r = await fetch(base + p);
    assert.equal(r.status, 403, p);
    assert.doesNotMatch(await r.text(), /"token"/, p);
  }
  // the link sets a cookie for this port, and the cookie alone is enough afterwards (a reload, the map's files)
  const first = await fetch(link);
  assert.equal(first.status, 200);
  const cookie = first.headers.get('set-cookie');
  assert.match(cookie, new RegExp(`^fp_${new URL(base).port}=${key}; Path=/; HttpOnly; SameSite=Lax$`));
  const pair = cookie.split(';')[0];
  assert.equal((await fetch(base + '/', { headers: { cookie: pair } })).status, 200);
  assert.equal((await fetch(base + '/graph.json', { headers: { cookie: pair } })).status, 200);
  assert.equal((await fetch(base + '/', { headers: { cookie: pair.replace(/.$/, 'x') } })).status, 403);
  // the cache folder stays unserved even with the key
  assert.equal((await fetch(base + '/.cache/key', { headers: { cookie: pair } })).status, 404);
});

test('the server\'s token and page key are readable by this account only', { skip: process.platform === 'win32' }, () => {
  const cache = path.join(root, 'floorplan', '.cache');
  assert.equal(fs.statSync(cache).mode & 0o777, 0o700);
  assert.equal(fs.statSync(path.join(cache, 'server.json')).mode & 0o777, 0o600);
  assert.equal(fs.statSync(path.join(cache, 'key')).mode & 0o777, 0o600);
});

test('API calls with the token from the map itself work', async () => {
  const r = await api('/api/flows', { headers: { 'x-floorplan-token': token } });
  assert.equal(r.status, 200);
  assert.deepEqual(await r.json(), { flows: [] });
});

test('files outside the map folder are never served', async () => {
  // including a neighbouring folder whose name starts with "floorplan"
  fs.mkdirSync(path.join(root, 'floorplan-old'));
  fs.writeFileSync(path.join(root, 'floorplan-old', 'notes.txt'), 'private notes');
  for (const p of ['/../shop-api/config.js', '/%2e%2e/shop-api/config.js', '/..%2fshop-api%2fconfig.js', '/..%2ffloorplan-old%2fnotes.txt']) {
    const r = await fetch(base + p, { headers: opened() });
    const body = await r.text();
    assert.equal(r.status, 404, p);
    assert.ok(!body.includes('DB_PASSWORD') && !body.includes('private notes'), `${p} -> ${r.status}`);
  }
});

test('a malformed address gets an error, and the server keeps running', async () => {
  assert.equal((await fetch(base + '/%E0%A4%A', { headers: opened() })).status, 400);
  assert.equal((await fetch(mapLink(root))).status, 200);
});
