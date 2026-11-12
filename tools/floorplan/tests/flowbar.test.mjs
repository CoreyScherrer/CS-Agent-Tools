import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';

const html = readFileSync(new URL('../skills/floorplan/assets/viewer.html', import.meta.url), 'utf8');

test('the list of flows and the playing step share one left column, one width', () => {
  assert.match(html, /#flowdock \{ position: fixed; left: 8px; top: calc\(var\(--hh, 64px\) \+ 4px\); width: min\(320px, calc\(100% - 16px\)\);/);
  assert.match(html, /<div id="flowdock" hidden><section class="fd glass" id="fd-flows" hidden>.*<section class="fd glass" id="flowbar" hidden>/);
  assert.match(html, /fm\.classList\.remove\('glass'\); fdFlows\.append\(fm\);/);
  assert.doesNotMatch(html, /#flowmenu, #legend/);
  assert.match(html, /gap: 8px; z-index: 9; \} \/\* under the bar \(10\)/, 'the bar\'s menus open over the column');
});

test('each section collapses from the arrow at its top right', () => {
  assert.equal((html.match(/<button type="button" class="fd-tog" aria-expanded="true"/g) || []).length, 3); // Flows, the step, and the dockSection template
  assert.match(html, /#flowdock \.fd\.collapsed > :not\(\.fd-h\), #flowdock \.fd\.collapsed #flowmenu \{ display: none; \}/);
  assert.match(html, /const b = ev\.target\.closest\('\.fd-tog'\); if \(!b\) return;\n  const shut = b\.closest\('\.fd'\)\.classList\.toggle\('collapsed'\);/);
});

test('the list stays open while a flow plays and marks the one playing', () => {
  assert.match(html, /function closeFlows\(\) \{ if \(!state\.flow\) fm\.classList\.remove\('open'\); \}/);
  assert.doesNotMatch(html, /r\.onclick = \(\) => \{ fm\.classList\.remove\('open'\); startFlow/);
  assert.match(html, /r\.classList\.toggle\('on', r\.dataset\.flow === f\.id\)/);
  assert.match(html, /\(fm\.classList\.contains\('open'\) && !state\.flow\)/, 'Escape still exits a playing flow');
  assert.match(html, /function stopFlow\(\) \{[^\n]*fdFlows\.classList\.remove\('collapsed'\)/, 'exiting a flow opens the list again next time');
  assert.match(html, /\$\('#fb-body'\)\.innerHTML = `<div class="ft"><div class="fk">\$\{h\(f\.title\)\}<\/div>/, 'the step card names its flow');
  assert.match(html, /freeArea\(\)\.x === 16 && stageRect\(\)\.bottom - \(\$\('header'\)\.offsetHeight \+ 4 \+ dock\.offsetHeight\) < 260\) \{ fdFlows\.classList\.add\('collapsed'\)/, 'a cramped window folds the list away');
  assert.ok(html.indexOf("$('#fl-x').onclick = stopFlow;") < html.indexOf('freeArea().x === 16 && stageRect()'), 'the room check runs after the step is filled in');
});

test('the map keeps clear of the column and shows both step boxes', () => {
  assert.match(html, /const b = \$\('#flowdock'\)\.getBoundingClientRect\(\), side = b\.right - r\.left \+ 16;/);
  assert.match(html, /if \(!sheet && r\.width - panelW - side - 16 >= 200\) left = side; else top = Math\.max\(top, \$\('header'\)\.offsetHeight \+ 4 \+ b\.height - r\.top \+ 8\);/);
  assert.match(html, /showBoxes\(\[pa, pb\]\);/);
});

test('every inline script in the viewer parses', () => {
  for (const [, code] of html.matchAll(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/g)) {
    try { new Function(code); } catch (e) { if (!/import|export|await/.test(e.message)) throw e; }
  }
});

const tour = readFileSync(new URL('../skills/floorplan/assets/ui/40-tour.js', import.meta.url), 'utf8');

test('the tour card is a card in the same left column', () => {
  assert.match(html, /dockSection: \(opts\) => dockSection\(opts\),/);
  assert.match(tour, /const card = SC\.dockSection\(\{ id: 'tour', title: 'Start here', label: 'the tour' \}\);/);
  assert.doesNotMatch(tour, /#tour \{ position: fixed;/);
  assert.match(tour, /card\.querySelector\('\.fd-tog'\)\.before\(closeBtn\);/, 'its close button sits beside the arrow');
});

test('each card scrolls on its own and the map stays clear of the column', () => {
  assert.match(html, /#flowdock \.fd-b \{ min-height: 0; overflow: auto; overscroll-behavior: contain; \}/);
  assert.match(html, /#flowdock #flowmenu \{[^}]*min-height: 0; overflow: auto; overscroll-behavior: contain;/);
  assert.doesNotMatch(html, /#flowdock #flowmenu \{[^}]*max-height: 40vh/);
  assert.match(html, /if \(!\$\('#flowdock'\)\.hidden\) \{/, 'the map keeps clear whenever the column shows, not only during a flow');
  assert.match(html, /function clearColumn\(\) \{/);
  assert.match(html, /if \(!behind\) return;\n  const dx = side \? col\.r - col\.l : 0, dy = side \? 0 : col\.b - col\.t;/, 'the map moves by the column\'s size, never further');
  assert.match(html, /if \(cleared\) return; \/\/ once per opening/, 'it moves once per opening, not again as the column grows');
  assert.match(html, /else if \(same\(cleared\)\) setT\(\{ k, x: x - cleared\.dx, y: y - cleared\.dy \}, true\);/, 'closing the column puts the map back');
  assert.match(html, /if \(same\(placed\?\.t\)\) placed\.fn\(true\);/, 'a fit made around the column is redone for the full width when it closes');
  assert.match(html, /placedAround\(fit\);/); assert.match(html, /placedAround\(home\);/);
  assert.match(html, /new ResizeObserver\(\(\) => \{ clearColumn\(\);/);
});
