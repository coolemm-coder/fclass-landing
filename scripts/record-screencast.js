/**
 * Meta App Review — Автозапись скринкастов через Playwright
 *
 * Записывает 2 видео:
 *  1. instagram_business_basic  (~60 сек)
 *  2. instagram_business_manage_messages  (~90 сек)
 *
 * Использует твой Chrome-профиль — не нужно заново логиниться.
 *
 * Запуск:
 *   node scripts/record-screencast.js
 */

const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

// ─── Конфиг ────────────────────────────────────────────────
const APP_ID      = '987255807812535';
const SUBMISSION  = '987270334477749';
const WORKFLOW_ID = 's9Ywcb4QkN1jRfyb';
const WEBHOOK_URL = 'https://emikss.host/webhook/fc-instagram-dm';
const N8N_URL     = 'https://emikss.host';
const TG_URL      = 'https://web.telegram.org/k/';

// Comet (Perplexity browser) — там залогинен Instagram Даши
const CHROME_PROFILE_DIR = path.join(process.env.HOME, 'Library/Application Support/Comet');
const COMET_EXEC = '/Applications/Comet.app/Contents/MacOS/Comet';

const OUTPUT_DIR = path.join(__dirname, '../data/screencasts');
fs.mkdirSync(OUTPUT_DIR, { recursive: true });

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function smoothScroll(page, distance = 500) {
  await page.evaluate(d => window.scrollBy({ top: d, behavior: 'smooth' }), distance);
  await sleep(1200);
}

// Отправляем тестовый IG DM вебхук
async function sendTestDM(page) {
  const timestamp = Date.now();
  const payload = {
    object: 'instagram',
    entry: [{
      id: '17841443163477494',
      time: Math.floor(timestamp / 1000),
      messaging: [{
        sender:    { id: '6823941070982134' },
        recipient: { id: '17841443163477494' },
        timestamp,
        message: {
          mid: `test_review_${timestamp}`,
          text: 'Привет! Хочу тур в Египет на 2 взрослых в июле, бюджет ~$2000. Какие варианты?'
        }
      }]
    }]
  };

  const result = await page.evaluate(async ({ url, body }) => {
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      return { ok: res.ok, status: res.status };
    } catch (e) {
      return { ok: false, error: e.message };
    }
  }, { url: WEBHOOK_URL, body: payload });

  console.log('  Вебхук:', result.ok ? `✅ ${result.status}` : `❌ ${result.error || result.status}`);
}

// Находим последний созданный .webm в папке и переименовываем
function renameLatestWebm(newName, excludePrefix) {
  const files = fs.readdirSync(OUTPUT_DIR)
    .filter(f => f.endsWith('.webm') && (!excludePrefix || !f.startsWith(excludePrefix)));
  if (!files.length) { console.log('  ⚠️  Видео-файл не найден'); return; }
  const latest = files
    .map(f => ({ f, t: fs.statSync(path.join(OUTPUT_DIR, f)).mtimeMs }))
    .sort((a, b) => b.t - a.t)[0];
  const dest = path.join(OUTPUT_DIR, newName);
  fs.renameSync(path.join(OUTPUT_DIR, latest.f), dest);
  const sizeMb = (fs.statSync(dest).size / 1024 / 1024).toFixed(1);
  console.log(`  ✅ Сохранено: ${newName} (${sizeMb} MB)`);
}

// ─── ВИДЕО 1: instagram_business_basic ─────────────────────
async function recordVideo1() {
  console.log('\n▶  Видео 1: instagram_business_basic (~60 сек)');

  // launchPersistentContext возвращает BrowserContext напрямую
  const ctx = await chromium.launchPersistentContext(CHROME_PROFILE_DIR, {
    executablePath: COMET_EXEC,
    headless: false,
    recordVideo: { dir: OUTPUT_DIR, size: { width: 1440, height: 900 } },
    viewport: null,
    args: ['--start-maximized', '--no-first-run'],
    ignoreDefaultArgs: ['--enable-automation'],
  });

  const page = await ctx.newPage();

  console.log('  → Meta App Settings');
  await page.goto(`https://developers.facebook.com/apps/${APP_ID}/settings/basic/`, { waitUntil: 'networkidle' });
  await sleep(3000);
  await smoothScroll(page, 400);
  await sleep(2000);

  console.log('  → Instagram Business');
  await page.goto(`https://developers.facebook.com/apps/${APP_ID}/instagram-business/`, { waitUntil: 'networkidle' });
  await sleep(4000);
  await smoothScroll(page, 300);
  await sleep(2000);

  console.log('  → Webhooks');
  await page.goto(`https://developers.facebook.com/apps/${APP_ID}/webhooks/`, { waitUntil: 'networkidle' });
  await sleep(4000);

  console.log('  → App Review form');
  await page.goto(
    `https://developers.facebook.com/apps/${APP_ID}/app-review/submissions/?submission_id=${SUBMISSION}&business_id=5010918918978380`,
    { waitUntil: 'networkidle' }
  );
  await sleep(4000);
  await smoothScroll(page, 300);
  await sleep(3000);

  await ctx.close();
  renameLatestWebm('instagram_business_basic.webm', null);
}

// ─── ВИДЕО 2: instagram_business_manage_messages ───────────
async function recordVideo2() {
  console.log('\n▶  Видео 2: instagram_business_manage_messages (~90 сек)');

  const ctx = await chromium.launchPersistentContext(CHROME_PROFILE_DIR, {
    executablePath: COMET_EXEC,
    headless: false,
    recordVideo: { dir: OUTPUT_DIR, size: { width: 1440, height: 900 } },
    viewport: null,
    args: ['--start-maximized', '--no-first-run'],
    ignoreDefaultArgs: ['--enable-automation'],
  });

  const page = await ctx.newPage();

  // 1. n8n — показываем workflow
  console.log('  → n8n workflow');
  await page.goto(`${N8N_URL}/workflow/${WORKFLOW_ID}`, { waitUntil: 'networkidle' });
  await sleep(5000);

  // 2. Отправляем тестовый DM
  console.log('  → Отправка тестового DM...');
  await sendTestDM(page);
  await sleep(3000);

  // 3. Показываем историю выполнений
  console.log('  → n8n executions');
  const page2 = await ctx.newPage();
  await page2.goto(`${N8N_URL}/workflow/${WORKFLOW_ID}/executions`, { waitUntil: 'networkidle' });
  await sleep(5000);
  await page2.bringToFront();

  // Кликаем на последнее выполнение чтобы показать детали
  try {
    await page2.click('table tbody tr:first-child', { timeout: 4000 });
    await sleep(4000);
  } catch (_) {
    await sleep(2000);
  }

  // 4. Telegram Web — показываем уведомление
  console.log('  → Telegram Web');
  const page3 = await ctx.newPage();
  await page3.goto(TG_URL, { waitUntil: 'networkidle' });
  await sleep(8000);
  await page3.bringToFront();
  await sleep(4000);

  // 5. Возвращаемся в n8n для финала
  await page2.bringToFront();
  await sleep(3000);

  await ctx.close();
  renameLatestWebm('instagram_business_manage_messages.webm', 'instagram_business_basic');
}

// ─── MAIN ──────────────────────────────────────────────────
(async () => {
  console.log('================================================');
  console.log('  Meta App Review — Playwright Screencast');
  console.log('================================================');
  console.log('\nИспользую Chrome-профиль (уже залогинен)...\n');

  await recordVideo1();

  console.log('\n  Пауза 3 сек перед видео 2...');
  await sleep(3000);

  await recordVideo2();

  console.log('\n================================================');
  console.log('  ГОТОВО!');
  console.log('================================================');
  const files = fs.readdirSync(OUTPUT_DIR).filter(f => f.endsWith('.webm'));
  files.forEach(f => {
    const size = (fs.statSync(path.join(OUTPUT_DIR, f)).size / 1024 / 1024).toFixed(1);
    console.log(`  📹 ${f} (${size} MB)`);
  });
  console.log(`\n  Папка: ${OUTPUT_DIR}`);
  console.log('\nЗагрузи в Meta App Review → Секция 3:');
  console.log(`  https://developers.facebook.com/apps/${APP_ID}/app-review/submissions/?submission_id=${SUBMISSION}`);
})().catch(err => {
  console.error('\n❌ Ошибка:', err.message);
  process.exit(1);
});
