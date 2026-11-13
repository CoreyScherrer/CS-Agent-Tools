// The map comes first on a computer too: details closed until a box is picked, the overview folded
// to one line, and no tour that restarts on every visit where the page can't remember it ran.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const assets = path.join(here, '..', 'skills', 'floorplan', 'assets');
const html = fs.readFileSync(path.join(assets, 'viewer.html'), 'utf8');
const tour = fs.readFileSync(path.join(assets, 'ui', '40-tour.js'), 'utf8');

test('the details start closed unless someone chose to keep them open', () => {
  assert.match(html, /document\.body\.classList\.toggle\('no-panel', isPhone\(\) \|\| !store\.get\('panel', false\)\);/);
});

test('picking a box opens its details without re-fitting the map or saving the choice', () => {
  assert.match(html, /const setPanel = \(on, \{ keepView = false \} = \{\}\) => \{/);
  assert.match(html, /if \(sel && document\.body\.classList\.contains\('no-panel'\)\) \{ setPanel\(true, \{ keepView: true \}\);/);
});

test('a shared link to a box opens its details on any screen', () => {
  assert.match(html, /if \(init\.s\) \{ document\.body\.classList\.remove\('no-panel'\);/);
});

test('the store says whether it can remember anything', () => {
  assert.match(html, /const store = \{ ok: \(\(\) => \{ try \{ localStorage\.setItem\('floorplan:probe', '1'\); localStorage\.removeItem\('floorplan:probe'\); return true; \} catch \{ return false; \} \}\)\(\),/);
});

test('the tour starts on its own only where the page can remember that it ran', () => {
  assert.match(tour, /if \(!SC\.store\.ok \|\| SC\.store\.get\(SEEN, false\) \|\| location\.hash\.length > 1\) return;/);
});
