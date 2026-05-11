#!/usr/bin/env node
/**
 * Blog Article Generator — First Class
 *
 * Использование:
 *   node scripts/blog-generator.js --keyword "деловые поездки" --title "Заголовок статьи" --slug "delovye-poezdki"
 *
 * Что делает:
 *   1. Исследует тему через Claude API + web_search (актуальные данные)
 *   2. Генерирует SEO-статью на основе найденных данных
 *   3. Сохраняет HTML в fclass-landing/blog/
 *   4. Добавляет URL в sitemap.xml
 *   5. Деплоит на Vercel
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// --- Config ---
const BLOG_DIR = path.join(__dirname, '../fclass-landing/blog');
const SITEMAP_PATH = path.join(__dirname, '../fclass-landing/sitemap.xml');
const LANDING_DIR = path.join(__dirname, '../fclass-landing');
const ANTHROPIC_API_KEY = process.env.ANTHROPIC_API_KEY;
const TODAY = new Date().toISOString().split('T')[0];
const CURRENT_YEAR = new Date().getFullYear();

// --- Args ---
const args = process.argv.slice(2);
const getArg = (name) => {
  var idx = args.indexOf('--' + name);
  return idx !== -1 ? args[idx + 1] : null;
};

const keyword  = getArg('keyword');
const title    = getArg('title');
const slug     = getArg('slug');
const skipDeploy = args.includes('--no-deploy');
const skipResearch = args.includes('--no-research');

if (!keyword || !title || !slug) {
  console.error('Usage: node blog-generator.js --keyword "запрос" --title "Заголовок" --slug "url-slug"');
  console.error('Options: --no-deploy, --no-research');
  process.exit(1);
}

var outputFile   = path.join(BLOG_DIR, slug + '.html');
var canonicalUrl = 'https://fclass.by/blog/' + slug + '.html';

// --- Claude API helper ---
function callClaude(payload, callback) {
  if (!ANTHROPIC_API_KEY) {
    console.error('Error: ANTHROPIC_API_KEY не задан');
    process.exit(1);
  }
  var body = JSON.stringify(payload);
  var options = {
    hostname: 'api.anthropic.com',
    path: '/v1/messages',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
      'anthropic-beta': 'web-search-2025-03-05',
      'Content-Length': Buffer.byteLength(body)
    }
  };
  var req = https.request(options, function(res) {
    var data = '';
    res.on('data', function(c) { data += c; });
    res.on('end', function() {
      try {
        callback(null, JSON.parse(data));
      } catch(e) {
        callback(e);
      }
    });
  });
  req.on('error', callback);
  req.write(body);
  req.end();
}

// --- Phase 1: Research ---
function research(callback) {
  if (skipResearch) {
    console.log('Исследование пропущено (--no-research).');
    return callback(null, '');
  }

  console.log('🔍 Исследую тему: "' + title + '"...');

  var payload = {
    model: 'claude-sonnet-4-6',
    max_tokens: 3000,
    tools: [{
      type: 'web_search_20250305',
      name: 'web_search',
      max_uses: 5
    }],
    system: 'Ты исследователь. Собери актуальные факты по теме для статьи на белорусском рынке. ' +
            'Год: ' + CURRENT_YEAR + '. Фокус: Беларусь, Минск, деловые поездки. ' +
            'Ищи на русском языке. Верни структурированный список фактов — только проверенные данные с источниками.',
    messages: [{
      role: 'user',
      content: 'Найди актуальные данные для статьи "' + title + '" (ключевой запрос: "' + keyword + '"). ' +
               'Нужно: актуальные нормы/правила/цифры для Беларуси в ' + CURRENT_YEAR + ' году. ' +
               'Сделай 3-4 поисковых запроса и собери факты.'
    }]
  };

  callClaude(payload, function(err, resp) {
    if (err) {
      console.warn('Ошибка исследования, продолжаю без него:', err.message);
      return callback(null, '');
    }
    if (resp.error) {
      console.warn('Claude research error:', resp.error.message);
      return callback(null, '');
    }

    // Собрать текст из всех text блоков
    var facts = '';
    (resp.content || []).forEach(function(block) {
      if (block.type === 'text') facts += block.text + '\n';
    });

    console.log('✅ Исследование завершено. Найдено данных: ' + facts.length + ' символов');
    callback(null, facts);
  });
}

// --- Phase 2: Write article ---
function writeArticle(researchData, callback) {
  console.log('✍️  Пишу статью...');

  var researchSection = researchData
    ? '\n\nАКТУАЛЬНЫЕ ДАННЫЕ (из веб-поиска ' + CURRENT_YEAR + '):\n' + researchData
    : '';

  var userPrompt = 'Напиши полную SEO-статью в HTML для блога fclass.by.\n\n' +
    'Тема: "' + title + '"\n' +
    'Главный ключевой запрос: "' + keyword + '"\n' +
    'Canonical URL: ' + canonicalUrl + '\n' +
    'Дата публикации: ' + TODAY + '\n' +
    researchSection + '\n\n' +
    'Требования к HTML:\n' +
    '1. Полный DOCTYPE html документ\n' +
    '2. <head>: Yandex.Metrika 107237229, canonical, meta description/keywords, og-теги, favicon (.ico + .png 120x120)\n' +
    '3. Schema.org: BreadcrumbList + BlogPosting + FAQPage (3 вопроса)\n' +
    '4. Google Fonts: DM Sans + Playfair Display\n' +
    '5. CSS переменные: --primary #0c1825, --accent #c9a962, --primary-light #1a3a5c\n' +
    '6. NAV: Услуги(/#services), Визы(/visa-support/), О нас(/#expertise), Блог(/blog/), Контакты(/#contact)\n' +
    '7. Структура: article-hero → breadcrumbs → .article (2000+ слов) → cta-box → related → footer\n' +
    '8. Компоненты: .info-table, .checklist[data-step], .tip-box, .warning-box, .cta-box, .related-grid\n' +
    '9. Footer: ссылки на разделы, TG: t.me/firstclassby, WA: wa.me/375447725266\n' +
    '10. Мобильная адаптация 768px/1024px\n\n' +
    'Контакты First Class: тел +375 44 772-52-66, email marketing@fclass.by\n' +
    'Related статьи: /blog/organizaciya-komandirovok.html, /blog/vizovaya-podderzhka-minsk.html\n\n' +
    'Верни ТОЛЬКО HTML код.';

  var payload = {
    model: 'claude-sonnet-4-6',
    max_tokens: 8000,
    system: 'Ты SEO-копирайтер для турагентства First Class (Минск, Беларусь). ' +
            'Пишешь статьи для блога fclass.by — сайта под корпоративные командировки. ' +
            'Стиль: профессиональный, конкретный, без воды. ' +
            'Используй актуальные данные из исследования. Не выдумывай цифры.',
    messages: [{ role: 'user', content: userPrompt }]
  };

  callClaude(payload, function(err, resp) {
    if (err) return callback(err);
    if (resp.error) return callback(new Error(resp.error.message));
    var html = (resp.content[0] || {}).text || '';
    html = html.replace(/^```html\n?/, '').replace(/\n?```$/, '');
    callback(null, html);
  });
}

// --- Update sitemap ---
function updateSitemap() {
  var sitemap = fs.readFileSync(SITEMAP_PATH, 'utf8');
  if (sitemap.includes(canonicalUrl)) {
    console.log('Sitemap: URL уже существует.');
    return;
  }
  var entry = '    <url><loc>' + canonicalUrl + '</loc><lastmod>' + TODAY + '</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>';
  sitemap = sitemap.replace('</urlset>', entry + '\n</urlset>');
  fs.writeFileSync(SITEMAP_PATH, sitemap, 'utf8');
  console.log('✅ Sitemap обновлён.');
}

// --- Deploy ---
function deploy() {
  if (skipDeploy) { console.log('Deploy пропущен.'); return; }
  console.log('🚀 Деплой на Vercel...');
  try {
    execSync('cd ' + LANDING_DIR + ' && npx vercel --prod --yes 2>&1', { encoding: 'utf8', timeout: 120000, stdio: 'inherit' });
  } catch(e) {
    console.error('Deploy ошибка:', e.message);
  }
}

// --- Main ---
research(function(err, facts) {
  writeArticle(facts, function(err, html) {
    if (err) { console.error('Ошибка генерации:', err.message); process.exit(1); }

    fs.writeFileSync(outputFile, html, 'utf8');
    console.log('✅ Статья сохранена: ' + outputFile);

    updateSitemap();
    deploy();

    console.log('\n✅ Готово!');
    console.log('URL: ' + canonicalUrl);
  });
});
