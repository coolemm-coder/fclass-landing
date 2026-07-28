import path from 'node:path';
import { chromium } from 'playwright';

const root = path.resolve(import.meta.dirname, '..');
const target = 'https://automation.landingpro.by/webhook/fc-lead';
const legacyTarget = 'https://automation.landingpro.by/webhook/fclass-blog-lead';
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
let responseCase = 'success';

await page.route('https://automation.landingpro.by/webhook/**', async (route) => {
  if (responseCase === 'http-error') {
    await route.fulfill({ status: 502, contentType: 'application/json', body: JSON.stringify({ success: false }) });
    return;
  }
  if (responseCase === 'rejected') {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: false }) });
    return;
  }
  if (responseCase === 'invalid-json') {
    await route.fulfill({ status: 200, contentType: 'text/plain', body: 'not-json' });
    return;
  }
  if (responseCase === 'legacy-success') {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true }) });
    return;
  }
  await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: true }) });
});

await page.addScriptTag({ path: path.join(root, 'assets/lead-webhook-guard.js') });

async function resultFor(url) {
  return page.evaluate(async (requestUrl) => {
    try {
      await fetch(requestUrl, { method: 'POST', body: new FormData() });
      return 'resolved';
    } catch (error) {
      return 'rejected';
    }
  }, url);
}

const expected = [
  ['success', target, 'resolved'],
  ['http-error', target, 'rejected'],
  ['rejected', target, 'rejected'],
  ['invalid-json', target, 'rejected'],
  ['legacy-success', legacyTarget, 'resolved']
];

const failures = [];
for (const [testCase, url, wanted] of expected) {
  responseCase = testCase;
  const actual = await resultFor(url);
  if (actual !== wanted) failures.push(testCase + ': expected ' + wanted + ', got ' + actual);
}

await browser.close();
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log('Verified lead guard runtime success and failure contracts.');
