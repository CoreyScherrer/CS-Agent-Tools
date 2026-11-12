// Admin look: the map's own top bar, panel and menus match the admin page that embeds it. One solid 60 px bar
// (logo and name, then the icon buttons, then search), 44 px icon buttons, the admin palette for the chrome in the
// dark theme only (the map's cards and lines keep their colours), and embed mode still hides and reports every button.
import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const assets = path.join(here, '..', 'skills', 'floorplan', 'assets');
const html = fs.readFileSync(path.join(assets, 'viewer.html'), 'utf8');
const theme = fs.readFileSync(path.join(assets, 'ui', '05-theme.js'), 'utf8');
const header = html.match(/<header>[\s\S]*?<\/header>/)[0];
const outsideMedia = html.replace(/@media [^{]*\{(?:[^{}]|\{[^{}]*\})*\}/g, '');

test('the bar reads left to right: logo, name and path, then the icon buttons, then search', () => {
  const at = (s) => header.indexOf(s);
  assert.ok(at('class="hl"') < at('class="hr"') && at('class="hr"') < at('class="hc"'), 'title, then buttons, then search');
  assert.ok(at('id="btn-up"') < at('class="hr"') && at('id="crumbs"') < at('class="hr"'), 'the Up arrow and breadcrumbs stay with the title');
  // the buttons in order: theme and the other extension buttons (#hdr-ext), Flows, Connections, details panel
  const order = ['id="hdr-ext"', 'id="flows-btn"', 'id="filters-btn"', 'id="btn-panel"'].map(at);
  assert.deepEqual([...order].sort((a, b) => a - b), order);
});

test('the bar is one solid 60 px row, not a see-through overlay', () => {
  assert.match(outsideMedia, /header \{ position: fixed; inset: 0 0 auto 0; height: 60px; display: flex; align-items: center;[^}]*background: var\(--bar-bg\); border-bottom: 1px solid var\(--bar-line\); \}/);
  assert.doesNotMatch(outsideMedia.match(/\nheader \{[^}]*\}/)[0], /gradient/);
});

test('the icon buttons are 44 px with 20 px icons, and the row scrolls instead of running under the search box', () => {
  assert.match(html, /header \.hr \.btn \{ position: relative; flex: none; width: 44px; height: 44px; padding: 0; justify-content: center; \}/);
  assert.match(html, /\.hr svg\.i \{ width: 20px; height: 20px; \}/);
  assert.match(theme, /#theme-toggle \{[^}]*width: 44px; height: 44px;/);
  assert.match(theme, /#theme-toggle svg \{ position: relative; width: 20px; height: 20px; \}/);
  assert.match(html, /\.hr \{[^}]*min-width: 0; overflow-x: auto; overflow-y: hidden; scrollbar-width: none; \}/);
  assert.match(html, /\.hr::-webkit-scrollbar \{ display: none; \}/);
  assert.match(html, /#search-btn \{ width: min\(460px, 36vw\); height: 44px;/);
});

test('Flows and Connections menus are fixed under their button, so the scrolling row cannot clip them', () => {
  assert.match(html, /#legend \{ position: fixed; top: calc\(var\(--hh, 60px\) \+ 4px\); left: var\(--mx, 8px\);/);
  assert.match(html, /const dropUnder = \(menu, btn\) => \{[^\n]*if \(menu\.classList\.contains\('open'\) && r\.width\) menu\.style\.setProperty\('--mx'/);
  assert.match(html, /fm\.classList\.toggle\('open'\); dropUnder\(fm, ev\.currentTarget\);/);
  assert.match(html, /legendEl\.classList\.toggle\('open'\); dropUnder\(legendEl, ev\.currentTarget\);/);
});

test('the dark theme carries the admin palette from the design tokens', () => {
  const block = html.match(/\n:root:not\(\[data-theme="light"\]\) \{([\s\S]*?)\n\}/)[1];
  const want = {
    '--admin-bg': '#060610', '--admin-surface': '#1a1a24', '--admin-surface-raised': '#12121a', '--admin-border': '#2a2a3a',
    '--admin-text': '#e0e0e0', '--admin-text-strong': '#fff', '--admin-text-subtle': '#9ca3af',
    '--admin-accent': '#6f42c1', '--admin-accent-light': '#8b5cf6', '--admin-accent-subtle': 'rgba(111, 66, 193, .15)',
    '--admin-border-subtle': 'rgba(var(--ink), .06)', // white at 6% in dark
  };
  for (const [k, v] of Object.entries(want)) assert.ok(block.includes(`${k}: ${v};`), `${k} is ${v}`);
  assert.match(block, /--bar-bg: var\(--admin-surface\); --bar-line: var\(--admin-border\);/);
});

test('only the chrome takes the admin palette, through the variables the existing rules already use; the map keeps its colours', () => {
  const scope = html.match(/:root:not\(\[data-theme="light"\]\) :is\(([^)]*)\) \{([\s\S]*?)\n\}/);
  assert.ok(scope, 'one scoped block');
  for (const part of ['header', '#panel', '.menu', '#palette', '#modal', '#toast', '#zoom', '#ask']) assert.ok(scope[1].split(', ').includes(part), `${part} is in it`);
  for (const v of ['--elev', '--surface', '--text', '--text-3', '--hair', '--menu-solid', '--palette-bg', '--modal-bg', '--on', '--ring']) assert.match(scope[2], new RegExp(`${v}: var\\(--admin-`), `${v} comes from the admin palette`);
  assert.match(scope[2], /--shadow-float: 0 0 0 1px var\(--admin-border\)/); // the 1 px admin border round menus and panels
  assert.doesNotMatch(scope[1], /\.card|\.node|\.edge|#stage|#svg/);
  // the map's own colours are untouched
  assert.match(html, /:root \{[^}]*--bg: #0f0f0f;[^}]*--surface: #191919;/);
  assert.match(html, /--k-http: #7aa7ff;/);
  assert.match(html, /--n-service: #b49cff;/);
  // the Screens menu is a .menu too, so it is covered
  assert.match(fs.readFileSync(path.join(assets, 'ui', '30-screens.js'), 'utf8'), /menu\.className = 'menu glass';/);
});

test('light keeps its own colours and gets the new bar', () => {
  assert.match(html, /:root\[data-theme="light"\] \{[^}]*--bar-bg: #ffffff; --bar-line: rgba\(0, 0, 0, \.09\);/);
  assert.doesNotMatch(html.match(/:root\[data-theme="light"\] \{([\s\S]*?)\n\}/)[1], /--admin-/);
});

test('embedded, the map keeps its see-through strip and hides and reports every button', () => {
  assert.match(html, /html\.embedded \.hc, html\.embedded \.hr > \.btn, html\.embedded \.hr > \.rel > \.btn, html\.embedded #hdr-ext \{ display: none !important; \}/);
  assert.match(html, /html\.embedded header \{ height: 64px;[^}]*border-bottom: 0; pointer-events: none; background: linear-gradient/);
  assert.match(html, /html\.embedded #legend \{ position: fixed; top: 8px; right: 8px; left: auto; \}/);
  // every button the bridge reports sits in .hc or .hr, where it looks
  const bridge = html.slice(html.indexOf('// Embedded: tell the page around the map'), html.indexOf('<!--__UI_EXTENSIONS__-->'));
  assert.match(bridge, /header\.querySelectorAll\('\.hc \.btn, \.hr \.btn'\)/);
  const hc = header.match(/<div class="hc">[\s\S]*?\n  <\/div>/)[0], hr = header.match(/<div class="hr">[\s\S]*?\n  <\/div>/)[0];
  assert.match(hc, /id="search-btn"/);
  for (const id of ['flows-btn', 'filters-btn', 'btn-panel']) assert.match(hr, new RegExp(`id="${id}"`));
  assert.match(hr, /<div id="hdr-ext" class="hr-ext"><\/div>/); // theme, recent, tour, screens, health, export are added here
  assert.match(html, /\$\('#hdr-ext'\)\.appendChild\(b\);/);
});
