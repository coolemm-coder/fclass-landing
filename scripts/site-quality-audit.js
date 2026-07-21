#!/usr/bin/env node

const fs = require('fs');
const http = require('http');
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..');
const DEFAULT_PAGES = [
  '/',
  '/komandirovki/',
  '/tickets/',
  '/tickets/aviabilety-dlya-yurlic/',
  '/resources/calculator/',
  '/tarify/',
  '/blog/',
  '/cases/',
  '/visa-support/',
  '/tickets/direct-flights/',
  '/tickets/minsk-moskva/',
  '/tickets/minsk-stambul/',
  '/tickets/minsk-baku/',
  '/tickets/minsk-kaliningrad/',
  '/komandirovki-na-vystavki/'
];

const VIEWPORTS = [
  ['mobile', { width: 390, height: 844 }],
  ['tablet', { width: 1024, height: 768 }],
  ['desktop', { width: 1440, height: 1000 }]
];

const FORBIDDEN_PATTERNS = [
  /15[–-]25%/i,
  /10[–-]25%/i,
  /15[–-]20%/i,
  /корпоративный договор/i,
  /НДС автоматически/i,
  /Окупаемость 1[–-]2/i,
  /скидк[аиуое]/i
];

const ABORTABLE_RESOURCE_TYPES = new Set(['image', 'media', 'font']);

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.pdf': 'application/pdf',
  '.webm': 'video/webm',
  '.mp4': 'video/mp4'
};

function stamp() {
  return new Date().toISOString().replace(/[:.]/g, '-');
}

function sanitizeName(value) {
  return value.replace(/^https?:\/\//, '').replace(/[^a-z0-9а-яё]+/gi, '-').replace(/^-|-$/g, '') || 'home';
}

function getPages() {
  if (process.env.AUDIT_PAGES) {
    return process.env.AUDIT_PAGES.split(',').map((p) => p.trim()).filter(Boolean);
  }

  if (process.env.AUDIT_SCOPE === 'sitemap') {
    const sitemap = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
    const pages = Array.from(sitemap.matchAll(/<loc>(.*?)<\/loc>/g))
      .map((m) => new URL(m[1]).pathname)
      .filter((p) => p === '/' || p.endsWith('/') || p.endsWith('.html'))
      .filter((p) => !p.includes('/tours/'))
      .filter((p) => !p.includes('/api/'));
    return Array.from(new Set(pages));
  }

  return DEFAULT_PAGES;
}

function resolvePublicPath(requestPath) {
  const urlPath = decodeURIComponent(requestPath.split('?')[0]);
  const safePath = path.normalize(urlPath).replace(/^(\.\.[/\\])+/, '');
  let filePath = path.join(ROOT, safePath);

  if (!filePath.startsWith(ROOT)) return null;
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, 'index.html');
  } else if (!fs.existsSync(filePath) && !path.extname(filePath)) {
    filePath = path.join(filePath, 'index.html');
  }
  if (!filePath.startsWith(ROOT) || !fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) return null;
  return filePath;
}

function startStaticServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const filePath = resolvePublicPath(req.url || '/');
      if (!filePath) {
        res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' });
        res.end('Not found');
        return;
      }
      const ext = path.extname(filePath).toLowerCase();
      res.writeHead(200, { 'content-type': MIME[ext] || 'application/octet-stream' });
      fs.createReadStream(filePath).pipe(res);
    });
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      resolve({ server, baseUrl: `http://127.0.0.1:${port}` });
    });
  });
}

function issue(level, code, message, data) {
  return { level, code, message, data: data || null };
}

function sameOrigin(baseUrl, targetUrl) {
  try {
    return new URL(baseUrl).origin === new URL(targetUrl).origin;
  } catch {
    return false;
  }
}

async function auditPage(browser, baseUrl, route, outDir) {
  const url = new URL(route, baseUrl).href;
  const pageIssues = [];
  const viewportResults = [];
  const resourceErrors = [];
  const requestFailures = [];
  const consoleErrors = [];

  const page = await browser.newPage();
  page.on('console', (msg) => {
    if (msg.type() === 'error') consoleErrors.push(msg.text());
  });
  page.on('response', (response) => {
    const status = response.status();
    const responseUrl = response.url();
    if (status >= 400 && sameOrigin(baseUrl, responseUrl)) {
      resourceErrors.push({ status, url: responseUrl });
    }
  });
  page.on('requestfailed', (request) => {
    const requestUrl = request.url();
    const resourceType = request.resourceType();
    const failure = request.failure() ? request.failure().errorText : 'failed';
    if (sameOrigin(baseUrl, requestUrl)) {
      if (ABORTABLE_RESOURCE_TYPES.has(resourceType) && failure.includes('ERR_ABORTED')) return;
      requestFailures.push({ url: requestUrl, error: failure, resourceType });
    }
  });

  let response;
  try {
    response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
  } catch (error) {
    await page.close();
    return {
      route,
      url,
      issues: [issue('error', 'NAVIGATION_FAILED', error.message)],
      viewports: []
    };
  }

  const status = response ? response.status() : 0;
  if (status >= 400 || status === 0) pageIssues.push(issue('error', 'HTTP_STATUS', `HTTP ${status}`));

  await page.waitForTimeout(500);

  const doc = await page.evaluate((forbiddenSources) => {
    const meta = (name) => document.querySelector(`meta[name="${name}"]`)?.getAttribute('content')?.trim() || '';
    const canonical = document.querySelector('link[rel="canonical"]')?.getAttribute('href')?.trim() || '';
    const title = document.title.trim();
    const description = meta('description');
    const h1s = Array.from(document.querySelectorAll('h1')).map((el) => el.textContent.trim().replace(/\s+/g, ' '));
    const jsonLdErrors = [];

    document.querySelectorAll('script[type="application/ld+json"]').forEach((script, index) => {
      try {
        JSON.parse(script.textContent || '');
      } catch (error) {
        jsonLdErrors.push(`JSON-LD #${index + 1}: ${error.message}`);
      }
    });

    const imagesMissingAlt = Array.from(document.querySelectorAll('img:not([alt])'))
      .slice(0, 10)
      .map((img) => img.getAttribute('src') || '(inline)');

    const targetBlankMissingRel = Array.from(document.querySelectorAll('a[target="_blank"]'))
      .filter((a) => {
        const rel = (a.getAttribute('rel') || '').toLowerCase();
        return !rel.includes('noopener') && !rel.includes('noreferrer');
      })
      .slice(0, 10)
      .map((a) => a.getAttribute('href') || a.textContent.trim());

    const visible = (el) => {
      const cs = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return cs.display !== 'none' && cs.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
    };

    const nonSemanticClickables = Array.from(document.querySelectorAll('[onclick]:not(a):not(button):not(input):not(select):not(textarea)'))
      .filter(visible)
      .slice(0, 10)
      .map((el) => ({
        tag: el.tagName.toLowerCase(),
        className: String(el.className || ''),
        role: el.getAttribute('role') || '',
        tabindex: el.getAttribute('tabindex') || ''
      }));

    const bodyText = document.body ? document.body.textContent || '' : '';
    const forbiddenHits = forbiddenSources
      .map((source) => {
        const match = bodyText.match(new RegExp(source, 'i'));
        return match ? match[0] : null;
      })
      .filter(Boolean);

    return {
      title,
      titleLength: title.length,
      description,
      descriptionLength: description.length,
      canonical,
      h1s,
      jsonLdCount: document.querySelectorAll('script[type="application/ld+json"]').length,
      jsonLdErrors,
      imagesMissingAlt,
      targetBlankMissingRel,
      nonSemanticClickables,
      forbiddenHits
    };
  }, FORBIDDEN_PATTERNS.map((pattern) => pattern.source));

  if (!doc.title) pageIssues.push(issue('error', 'TITLE_MISSING', 'Missing <title>'));
  if (doc.title && (doc.titleLength < 20 || doc.titleLength > 65)) {
    pageIssues.push(issue('warn', 'TITLE_LENGTH', `Title length ${doc.titleLength}`, doc.title));
  }
  if (!doc.description) pageIssues.push(issue('error', 'DESCRIPTION_MISSING', 'Missing meta description'));
  if (doc.description && (doc.descriptionLength < 80 || doc.descriptionLength > 170)) {
    pageIssues.push(issue('warn', 'DESCRIPTION_LENGTH', `Meta description length ${doc.descriptionLength}`, doc.description));
  }
  if (!doc.canonical) pageIssues.push(issue('error', 'CANONICAL_MISSING', 'Missing canonical URL'));
  if (doc.h1s.length !== 1) pageIssues.push(issue('error', 'H1_COUNT', `Expected 1 H1, found ${doc.h1s.length}`, doc.h1s));
  doc.jsonLdErrors.forEach((err) => pageIssues.push(issue('error', 'JSONLD_INVALID', err)));
  if (doc.imagesMissingAlt.length) pageIssues.push(issue('warn', 'IMAGE_ALT_MISSING', 'Images without alt', doc.imagesMissingAlt));
  if (doc.targetBlankMissingRel.length) pageIssues.push(issue('warn', 'TARGET_BLANK_REL', 'target=_blank links without noopener/noreferrer', doc.targetBlankMissingRel));
  if (doc.nonSemanticClickables.length) pageIssues.push(issue('warn', 'NON_SEMANTIC_CLICKABLE', 'Visible non-semantic onclick elements', doc.nonSemanticClickables));
  if (doc.forbiddenHits.length) pageIssues.push(issue('error', 'FORBIDDEN_COPY', 'Forbidden positioning/copy found', doc.forbiddenHits));

  for (const [viewportName, viewport] of VIEWPORTS) {
    await page.setViewportSize(viewport);
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(500);

    const metrics = await page.evaluate(() => {
      const fixedVisible = Array.from(document.querySelectorAll('.tg-bubble,.floating-buttons,.sticky-mobile-cta,.fc-burger'))
        .filter((el) => {
          const cs = getComputedStyle(el);
          const rect = el.getBoundingClientRect();
          return cs.display !== 'none' && cs.visibility !== 'hidden' && rect.width > 0 && rect.height > 0 && rect.bottom > 0 && rect.top < window.innerHeight;
        })
        .map((el) => {
          const rect = el.getBoundingClientRect();
          return {
            className: String(el.className || ''),
            position: getComputedStyle(el).position,
            x: Math.round(rect.x),
            y: Math.round(rect.y),
            width: Math.round(rect.width),
            height: Math.round(rect.height)
          };
        });

      const smallTargets = Array.from(document.querySelectorAll('a,button,input,select,textarea,[role="button"]'))
        .filter((el) => {
          const cs = getComputedStyle(el);
          const rect = el.getBoundingClientRect();
          return cs.display !== 'none' && cs.display !== 'inline' && cs.visibility !== 'hidden' && rect.width > 0 && rect.height > 0 && rect.top < window.innerHeight && rect.bottom > 0;
        })
        .filter((el) => {
          const rect = el.getBoundingClientRect();
          return rect.width < 36 || rect.height < 36;
        })
        .slice(0, 8)
        .map((el) => {
          const rect = el.getBoundingClientRect();
          return {
            tag: el.tagName.toLowerCase(),
            text: (el.textContent || el.getAttribute('aria-label') || '').trim().replace(/\s+/g, ' ').slice(0, 40),
            width: Math.round(rect.width),
            height: Math.round(rect.height)
          };
        });

      return {
        width: window.innerWidth,
        scrollWidth: document.documentElement.scrollWidth,
        overflow: Math.max(0, document.documentElement.scrollWidth - window.innerWidth),
        h1Count: document.querySelectorAll('h1').length,
        fixedVisible,
        smallTargets
      };
    });

    const screenshot = path.join(outDir, `${viewportName}-${sanitizeName(route)}.png`);
    await page.screenshot({ path: screenshot, fullPage: false });
    viewportResults.push({ viewport: viewportName, screenshot, ...metrics });

    if (metrics.overflow > 2) {
      pageIssues.push(issue('error', 'HORIZONTAL_OVERFLOW', `${viewportName}: overflow ${metrics.overflow}px`, metrics));
    }
    if (viewportName === 'mobile' && metrics.fixedVisible.filter((el) => !el.className.includes('fc-burger')).length > 1) {
      pageIssues.push(issue('warn', 'MOBILE_CTA_OVERLOAD', 'More than one fixed CTA/chat element visible on mobile', metrics.fixedVisible));
    }
    if (viewportName === 'mobile' && metrics.smallTargets.length) {
      pageIssues.push(issue('warn', 'SMALL_TOUCH_TARGETS', `${metrics.smallTargets.length} small above-fold touch targets`, metrics.smallTargets));
    }
  }

  resourceErrors.forEach((err) => pageIssues.push(issue('error', 'RESOURCE_ERROR', `${err.status} ${err.url}`)));
  requestFailures.forEach((err) => pageIssues.push(issue('error', 'REQUEST_FAILED', `${err.url} (${err.resourceType}): ${err.error}`)));
  consoleErrors.slice(0, 10).forEach((err) => pageIssues.push(issue('warn', 'CONSOLE_ERROR', err)));

  await page.close();

  return {
    route,
    url,
    status,
    title: doc.title,
    description: doc.description,
    canonical: doc.canonical,
    h1s: doc.h1s,
    jsonLdCount: doc.jsonLdCount,
    issues: pageIssues,
    viewports: viewportResults
  };
}

function toMarkdown(results, baseUrl) {
  const lines = [];
  const errors = results.flatMap((page) => page.issues.filter((item) => item.level === 'error'));
  const warnings = results.flatMap((page) => page.issues.filter((item) => item.level === 'warn'));
  lines.push(`# Site Quality Audit`);
  lines.push('');
  lines.push(`Base URL: ${baseUrl}`);
  lines.push(`Pages: ${results.length}`);
  lines.push(`Errors: ${errors.length}`);
  lines.push(`Warnings: ${warnings.length}`);
  lines.push('');

  for (const result of results) {
    lines.push(`## ${result.route}`);
    lines.push('');
    lines.push(`- Status: ${result.status || 'n/a'}`);
    lines.push(`- H1: ${result.h1s.length} (${result.h1s.join(' | ') || 'none'})`);
    lines.push(`- JSON-LD blocks: ${result.jsonLdCount}`);
    lines.push(`- Viewports: ${result.viewports.map((vp) => `${vp.viewport} overflow ${vp.overflow}px`).join(', ')}`);
    if (result.issues.length) {
      lines.push(`- Issues:`);
      for (const item of result.issues) {
        lines.push(`  - [${item.level.toUpperCase()}] ${item.code}: ${item.message}`);
      }
    } else {
      lines.push(`- Issues: none`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

async function main() {
  let server = null;
  let baseUrl = process.env.AUDIT_BASE_URL;
  if (!baseUrl) {
    const local = await startStaticServer();
    server = local.server;
    baseUrl = local.baseUrl;
  }

  const outDir = path.resolve(process.env.AUDIT_OUT_DIR || path.join('/tmp', `fclass-site-quality-${stamp()}`));
  fs.mkdirSync(outDir, { recursive: true });

  const pages = getPages();
  const browser = await chromium.launch({ headless: true });
  const results = [];

  for (const route of pages) {
    process.stdout.write(`Auditing ${route} ... `);
    const result = await auditPage(browser, baseUrl, route, outDir);
    results.push(result);
    const errors = result.issues.filter((item) => item.level === 'error').length;
    const warnings = result.issues.filter((item) => item.level === 'warn').length;
    console.log(errors ? `ERRORS ${errors}, warnings ${warnings}` : `ok, warnings ${warnings}`);
  }

  await browser.close();
  if (server) server.close();

  const summary = {
    baseUrl,
    generatedAt: new Date().toISOString(),
    pages: results.length,
    errorCount: results.reduce((sum, page) => sum + page.issues.filter((item) => item.level === 'error').length, 0),
    warningCount: results.reduce((sum, page) => sum + page.issues.filter((item) => item.level === 'warn').length, 0),
    results
  };

  fs.writeFileSync(path.join(outDir, 'summary.json'), JSON.stringify(summary, null, 2));
  fs.writeFileSync(path.join(outDir, 'report.md'), toMarkdown(results, baseUrl));

  console.log('');
  console.log(`Report: ${path.join(outDir, 'report.md')}`);
  console.log(`Summary: ${path.join(outDir, 'summary.json')}`);
  console.log(`Errors: ${summary.errorCount}`);
  console.log(`Warnings: ${summary.warningCount}`);

  if (summary.errorCount > 0) process.exit(1);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
