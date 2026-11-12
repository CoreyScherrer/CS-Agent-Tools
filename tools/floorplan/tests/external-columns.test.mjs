// A long list of outside services used to make one column several screens tall on the right.
// Past EXT_PER_COL they share out across up to three columns, using ELK layer partitions.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, '..', 'skills', 'floorplan', 'assets', 'viewer.html'), 'utf8');
const layout = html.slice(html.indexOf('async function layout('), html.indexOf('// ======================= render'));

test('outside services share out across up to three columns past seven', () => {
  assert.match(html, /const EXT_PER_COL = 7, EXT_COLS_MAX = 3;/);
  assert.match(layout, /const cols = view\.connectors\.length \? 1 : Math\.min\(EXT_COLS_MAX, Math\.ceil\(exts\.length \/ EXT_PER_COL\)\);/);
  assert.match(layout, /'elk\.partitioning\.partition': String\(1 \+ \(exts\.indexOf\(item\) % cols\)\)/);
  assert.match(layout, /\.\.\.\(cols > 1 \? \{ 'elk\.partitioning\.activate': 'true' \} : \{\}\)/);
});

test('a short list, or a view with connectors, keeps the single last column', () => {
  assert.match(layout, /: \{ 'elk\.layered\.layering\.layerConstraint': 'LAST' \};/);
});
