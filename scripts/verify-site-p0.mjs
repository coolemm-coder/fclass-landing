import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const excluded = new Set(['.git', '.github', 'node_modules', 'docs', 'web-panel']);
const failures = [];
let guardedPages = 0;

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.isDirectory() && excluded.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full);
      continue;
    }
    if (!entry.isFile() || !entry.name.endsWith('.html')) continue;
    if (full.endsWith('/mobile-preview.html')) continue;

    const source = fs.readFileSync(full, 'utf8');
    const usesInlineLeadWebhook = /automation\.landingpro\.by\/webhook\/(fc-lead|fclass-blog-lead|fclass-pdf-lead)/.test(source);
    const usesRouteHandler = source.includes('/tickets/route-page.js') && source.includes('class="route-form"');
    if (!usesInlineLeadWebhook && !usesRouteHandler) continue;

    guardedPages += 1;
    const guardPos = source.indexOf('/assets/lead-webhook-guard.js');
    const headEnd = source.indexOf('</head>');
    if (guardPos < 0 || headEnd < 0 || guardPos > headEnd) {
      failures.push(path.relative(root, full) + ': missing early lead guard');
    }
  }
}
walk(root);

const guard = fs.readFileSync(path.join(root, 'assets/lead-webhook-guard.js'), 'utf8');
for (const token of ['response.ok', 'result.success !== true', 'result.ok !== true', "mode: 'cors'", '12000']) {
  if (!guard.includes(token)) failures.push('lead guard missing ' + token);
}

const route = fs.readFileSync(path.join(root, 'tickets/route-page.js'), 'utf8');
if (route.includes("mode: 'no-cors'") || !route.includes("status.setAttribute('role', 'alert')")) {
  failures.push('route form does not expose verified success/error states');
}

for (const relative of [
  'tickets/minsk-dubai/index.html',
  'tickets/minsk-istanbul/index.html',
  'resources/calculator/index.html',
  'resources/dogovor-template/index.html'
]) {
  const source = fs.readFileSync(path.join(root, relative), 'utf8');
  if (/mode\s*:\s*['\"]no-cors['\"]/.test(source)) failures.push(relative + ': still uses no-cors');
  if (/\.finally\s*\(function\s*\(\)\s*\{\s*(form\.style\.display|document\.getElementById\(['\"]thanks)/.test(source)) {
    failures.push(relative + ': still reports success from finally');
  }
}

if (guardedPages < 55) failures.push('unexpectedly low guarded page count: ' + guardedPages);
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log('Verified ' + guardedPages + ' guarded lead pages and explicit lead success/error handling.');
