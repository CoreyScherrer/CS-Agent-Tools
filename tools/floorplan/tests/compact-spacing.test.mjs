// Boxes sit about half as far apart as before, and lines keep a little more room from a box's top and bottom.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const html = fs.readFileSync(path.join(here, '..', 'skills', 'floorplan', 'assets', 'viewer.html'), 'utf8');
const layout = html.slice(html.indexOf('async function layout('), html.indexOf('// ======================= render'));

test('boxes sit closer together across and down', () => {
  assert.match(layout, /'elk\.layered\.spacing\.nodeNodeBetweenLayers': '70'/);
  assert.match(layout, /'elk\.spacing\.nodeNode': '18'/);
  assert.match(layout, /'elk\.spacing\.componentComponent': '44'/);
});

test('lines keep more room from the top and bottom of a box', () => {
  assert.match(layout, /'elk\.spacing\.edgeNode': '18'/);
});
