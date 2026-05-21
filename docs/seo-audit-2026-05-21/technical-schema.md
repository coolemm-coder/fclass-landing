# fclass.by — Technical SEO & Schema Audit

**Date:** 2026-05-21
**Scope:** robots.txt, sitemap.xml, canonicals, duplicate content, security headers, JSON-LD/Schema, mobile-preview SEO risk, HTTP status/redirects.
**Source:** local committed HTML at `/Users/admin/Desktop/FirstClass_Automation/` (= live content); production on Beltelecom via FTP. Live checks against `https://fclass.by`.

---

## Severity Summary

| # | Finding | Severity |
|---|---------|----------|
| 1 | `mobile-preview.html` content parity gap (40% of desktop text) — mobile-first indexing risk | **High** |
| 2 | UA-sniffing serves different HTML to mobile vs desktop (cloaking-adjacent) | **Medium** |
| 3 | Missing security headers: HSTS, X-Frame-Options, CSP | **Medium** |
| 4 | `mobile-preview.html` schema/NAP inconsistency (`пр.` vs `просп.`, `, оф. 12` suffix) | **Medium** |
| 5 | TravelAgency schema missing `sameAs` (social/profile links) | **Medium** |
| 6 | `content/blog/fclass-blog-2026-04-01.html` canonical points to extensionless URL that 301s | **Low** |
| 7 | Sitemap: `lastmod` mass-stamped `2026-05-15`, low freshness signal | **Low** |
| 8 | Sitemap omits `cases/` legitimately-present? (it is present) — minor coverage notes below | **Low** |
| 9 | robots.txt `Host:` directive is non-standard (Yandex-only, ignored elsewhere) | **Low** |

No **Critical** issues found. Redirects, canonicals on public pages, and JSON-LD validity are all healthy.

---

## 1. robots.txt

Fetched `https://fclass.by/robots.txt`.

**Correct / good:**
- `User-agent: *` → `Allow: /` with sensible disallows for legacy Bitrix paths (`/bitrix/`, `/personal/`, `/auth/`, `/*.php$`) and faceted/query params (`?sort=`, `?page=`, `?filter=`, `?tags=`, `?q=`).
- **AI crawlers explicitly allowed** (good for GEO/AEO): `GPTBot`, `ChatGPT-User`, `ClaudeBot`, `PerplexityBot`, `Google-Extended` each have their own `Allow: /` block.
- `Sitemap: https://fclass.by/sitemap.xml` present.
- `Crawl-delay: 1` — harmless; ignored by Google, respected by Yandex/Bing.

**Issues:**
- **Low** — `Host: https://fclass.by` is a deprecated Yandex-only directive. It includes the scheme, which Yandex's spec does not expect (host only). Harmless but non-standard; can be removed.
- **Low** — Disallow blocks reference paths that may not exist on this static site (`/wp-admin/`, `/wp-content/`, `/cart/`, `/checkout/`, `/catalog/`, `/product/`, `/outlet/`). Defensive/harmless, but `/wp-*` suggests a copy-pasted template; no WordPress here.
- **Note:** Per-AI-crawler blocks reset the ruleset — `GPTBot` etc. do **not** inherit the `*` disallows. Since they get bare `Allow: /`, GPTBot can crawl `/bitrix/`, `?sort=` etc. that `*` blocks. Likely intended (full access for AI), but worth a conscious decision.

---

## 2. sitemap.xml

53 `<loc>` entries. Format valid (`urlset` + `xmlns` 0.9, each url has `loc/lastmod/changefreq/priority`).

### Coverage vs local public pages

Local public HTML (after excluding internal dirs and the `.htaccess`-gated artifacts):

**In sitemap and present locally — OK.** All 14 `tickets/*`, `komandirovki/`, `komandirovki-na-vystavki/`, `tickets/`, `concierge/`, `komandirovochnye-kalkulyator/`, `blog/`, all blog articles, `resources/calculator/`, `resources/dogovor-template/`, `cases/`, plus `llms.txt`. The home `/` is included.

**Pages present locally but MISSING from sitemap:**
| Local page | Note |
|---|---|
| `privacy/index.html` (`/privacy/`) | Intentional omission is fine (legal page), low value. |
| `tours/index.html` (`/tours/`) | Correctly omitted — `/tours/` 301s to `/tickets/` (confirmed live: `301 → /tickets/`). Good. |
| `carousels/2026/05/*.html` | Internal social-card artifacts; correct to omit. |
| `content/blog/fclass-blog-2026-04-01.html` | Draft/workspace copy; correct to omit (see Finding 6). |
| `blog/_template.html`, `firstclass-growth-playbook.html`, `firstclass-gtm-plan.html` | `.htaccess`-gated (G/410). Correctly omitted. |
| `mobile-preview.html` | Correctly omitted; it is the mobile body for `/`. |
| `blog/korporativnye-aviabilety-minsk/index.html` | Redirect stub (noindex) — correctly omitted. |

No genuinely-missing high-value page detected. **Sitemap coverage is good.**

**Orphaned sitemap URLs (in sitemap but no obvious local file):** none — all 53 map to a present page, a directory `index.html`, or `llms.txt`. `llms.txt` in a sitemap is unusual but harmless.

**Issues:**
- **Low** — `lastmod` is mass-stamped `2026-05-15` for ~45 of 53 URLs (only home, vystavki, erevan, polsha, batumi, kaliningrad/sochi/baku differ). Mass-identical lastmod is a weak/ignored freshness signal and can look templated. Set real per-file modification dates.
- **Low** — `priority` inflation: 30+ URLs at `0.9`+ dilutes the signal (priority is relative within a site). Cosmetic; Google largely ignores it.
- **Low** — `/tours/` is **not** in the sitemap (correct, it redirects) — confirms no index-bloat there.

---

## 3. Canonicals

Grepped all 56 public HTML files. Results:

**Healthy:**
- Every public page has exactly one `<link rel="canonical">`.
- All self-referencing and absolute `https://fclass.by/...`.
- **No `vercel.app` or wrong-domain canonicals** anywhere (grep returned zero). The earlier Vercel-preview concern is resolved.
- `mobile-preview.html` canonical → `https://fclass.by/` (correct — points to the desktop URL it is served under). Confirmed live: both iPhone and desktop UA at `/` emit `<link rel="canonical" href="https://fclass.by/">`.
- `tours/index.html` canonical → `https://fclass.by/tickets/` (cross-page canonical matching the 301 — consistent).

**Issues:**
- **Low / Finding 6** — `content/blog/fclass-blog-2026-04-01.html` line 12: canonical = `https://fclass.by/blog/komandirovki-belarus-2026` (extensionless, no `.html`). The live URL is `...belarus-2026.html`; the extensionless form would 301 (per `.htaccess` blog rules don't cover this exact case, but it's not the canonical .html). Since this file is a workspace copy under `/content/` (G-blocked by `.htaccess`), it is not served — **no live impact**, but the canonical value is wrong if it were ever published.
- `blog/_template.html` has a placeholder canonical `.../SLUG.html` — fine, template is gated.

---

## 4. Duplicate Content — `korporativnye-aviabilety-minsk`

- `blog/korporativnye-aviabilety-minsk.html` — the real article (374 lines).
- `blog/korporativnye-aviabilety-minsk/index.html` — **14-line redirect stub**: `<meta name="robots" content="noindex, follow">`, `<meta http-equiv="refresh" content="0; url=...">`, JS `location.replace`, **and** canonical → `.html`.

**Verdict: NOT a duplicate-content problem.** The directory version is a properly-handled redirect stub (noindex + canonical + JS/meta refresh both pointing to the canonical `.html`). Additionally `.htaccess` rule `^blog/([^/]+)/$ → /blog/$1.html [R=301]` means `/blog/korporativnye-aviabilety-minsk/` 301s server-side before the stub is even reached. Defense in depth. No canonical conflict.

**Minor note (Low):** the stub uses a meta-refresh + JS redirect, which is a weaker pattern than the server 301 already in place — it is redundant. Could be deleted entirely since `.htaccess` already 301s the trailing-slash form. Keeping it is harmless.

---

## 5. Security Headers

Live `curl -D -` on `https://fclass.by/` (HTTP/2 200, server nginx):

| Header | Present | Value |
|---|---|---|
| `X-Content-Type-Options` | ✅ | `nosniff` |
| `Referrer-Policy` | ✅ | `strict-origin-when-cross-origin` |
| `Strict-Transport-Security` (HSTS) | ❌ | **missing** |
| `X-Frame-Options` | ❌ | **missing** |
| `Content-Security-Policy` | ❌ | **missing** |
| `Permissions-Policy` | ❌ | missing |

Only the two headers set in `.htaccess` `mod_headers` block surface. Note HTTPS is terminated at nginx upstream (Apache only sees forwarded scheme), so HSTS would need to be added at the nginx layer or via the `mod_headers` block (with caution).

**Issues:**
- **Medium** — No **HSTS**. Recommend `Strict-Transport-Security: max-age=31536000; includeSubDomains` (after confirming all subdomains are HTTPS).
- **Medium** — No **X-Frame-Options** / `frame-ancestors`. Clickjacking exposure. Add `X-Frame-Options: SAMEORIGIN` or a CSP `frame-ancestors 'self'`.
- **Medium** — No **CSP**. For a static marketing site a basic policy is achievable; at minimum a report-only CSP is low-risk.
- **Low** — No `Permissions-Policy`. Optional hardening.

These are security/quality signals; modest indirect SEO/trust value.

---

## 6. Schema / JSON-LD

Extracted and JSON-parsed all `application/ld+json` blocks on key pages — **all parse as valid JSON** (no syntax errors anywhere checked).

| Page | Blocks | Types |
|---|---|---|
| `index.html` | 4 | TravelAgency, FAQPage, BreadcrumbList, Service |
| `mobile-preview.html` | 1 | TravelAgency only |
| `komandirovki/` | 2 | Service, FAQPage |
| `komandirovki-na-vystavki/` | 2 | Service, BreadcrumbList |
| `tickets/` | 3 | BreadcrumbList, Service, FAQPage |
| `tickets/minsk-stambul/` | 3 | BreadcrumbList, Service, FAQPage |
| `tickets/minsk-moskva/` | 3 | BreadcrumbList, Service, FAQPage |
| `blog/` | 2 | BreadcrumbList, Blog |
| `blog/komandirovka-v-uzbekistan-2026.html` | 3 | BlogPosting, FAQPage, BreadcrumbList |
| `blog/korporativnye-aviabilety-minsk.html` | 3 | BlogPosting, BreadcrumbList, FAQPage |

Site-wide type counts: `Organization` ×70 instances, `TravelAgency` ×18, `Service`, `FAQPage`, `BreadcrumbList`, `BlogPosting`/`Blog`, `LocalBusiness` ×1.

**index.html TravelAgency block** (primary entity):
- Has: name, alternateName, description, url, `telephone +375447725266`, email, foundingDate, address, geo (`53.909249, 27.548248`), openingHoursSpecification, `aggregateRating 5.0 / 44 ratings / 39 reviews`, priceRange, areaServed, serviceArea, hasOfferCatalog.
- Address: `просп. Победителей, 11` / Минск / 220004 / BY — **matches canonical NAP** (no "BC Royal Plaza", confirmed removed: grep found 0 occurrences).
- **Missing `sameAs`** — no links to social/messenger/maps profiles. (Medium)

**NAP / address consistency (Medium — Finding 4):**
JSON-LD `streetAddress` values across the site are **not uniform**:
- `просп. Победителей, 11` — index.html and others (canonical form ✅)
- `пр. Победителей, 11, оф. 12` — **mobile-preview.html** (abbreviation `пр.` differs; adds `, оф. 12`)
- `просп. Победителей, 11` — concierge variant

Body-text mentions also vary: `Победителей, 11` (×12), `Победителей 11`, `Победителей, 11, оф. 12`. The canonical per project rules is **«просп. Победителей, 11, оф. 12»**. Recommend normalizing all `streetAddress` and visible NAP to one exact string (decide whether `оф. 12` is included). Inconsistent NAP weakens local entity confidence.

**`telephone` is consistent** (`+375447725266` everywhere — good).

**`@type` mix (Low):** `concierge/index.html` uses `LocalBusiness` while the rest use `TravelAgency`. Consider standardizing the primary business entity to `TravelAgency` (subclass of LocalBusiness) for consistency, or keep deliberately. Also consider adding a dedicated `Organization`/`@id` node so the many `Organization` references resolve to one canonical entity (`@id` graph linking).

**Missing recommended schema (Low):**
- No `WebSite` + `SearchAction` (sitelinks search box) — optional, low ROI without on-site search.
- `BreadcrumbList` is absent on `komandirovki/` (has Service+FAQ only) — minor; add for consistency.

---

## 7. Mobile-preview SEO Risk

`.htaccess` mechanism **confirmed** (lines under "MOBILE USER-AGENT REWRITE 2026-05-12"):
```
RewriteCond %{HTTP_USER_AGENT} (iPhone|Android.*Mobile|Windows Phone|BlackBerry|Opera Mini|webOS) [NC]
RewriteCond %{HTTP_USER_AGENT} !iPad [NC]
RewriteCond %{REQUEST_URI} ^/$ [OR]
RewriteCond %{REQUEST_URI} ^/index\.html$
RewriteRule ^(index\.html)?$ /mobile-preview.html [L]
```
Phones (not tablets) requesting `/` get `mobile-preview.html` served **internally**; URL stays `/`. Direct hits to `/mobile-preview.html` 301 → `/` (confirmed live: `301 → https://fclass.by/`).

**mobile-preview.html SEO elements (present — good):**
- `<title>` present and **identical** to desktop: "Авиабилеты и командировки в Минске — авиакасса GDS | First Class".
- meta description ✅, viewport ✅, og:title ✅, robots `index, follow` ✅, **canonical → `https://fclass.by/`** ✅, single `<h1>` ✅.
- JSON-LD: 1 block (TravelAgency).

**Risks:**
- **High (Finding 1) — content parity gap.** Approx visible-text length: desktop `index.html` ≈ **14,850 chars**; `mobile-preview.html` ≈ **5,900 chars** (~40%). Desktop has **4 schema blocks** (TravelAgency + FAQPage + BreadcrumbList + Service); mobile has **only 1** (TravelAgency) — **FAQPage, BreadcrumbList and Service schema are absent on mobile**. Under **mobile-first indexing, Google indexes the mobile version**, so the FAQ rich-result eligibility, breadcrumb display, and ~60% of the homepage copy/internal links may be lost from the indexed page. This is the single most material SEO risk on the site.
- **Medium (Finding 2) — cloaking-adjacent.** Serving substantively different HTML by UA on the same URL is a gray area. Because the *intent* matches (same primary content/title, mobile is a lighter render, not deceptive) and canonical/robots are honest, hard-cloaking penalty risk is low — but the divergence in content depth and schema is exactly what mobile-first indexing penalizes. Preferred long-term fix: one responsive document instead of UA-forked HTML.
- **Medium (Finding 4)** — mobile schema has the divergent NAP (`пр. ...оф. 12`) noted above; the indexed (mobile) entity address differs from desktop.

**Recommendation:** bring mobile-preview to full content + schema parity (port FAQPage, BreadcrumbList, Service; expand body copy and internal links to match), and normalize NAP — or migrate to a single responsive page and retire the UA rewrite.

---

## 8. HTTP Status / Redirects (live spot-checks)

| URL | Result |
|---|---|
| `/` (desktop UA) | `HTTP/2 200` |
| `/` (iPhone UA) | `200`, serves mobile body, same title/canonical |
| `/tickets/minsk-istanbul/` | `301 → /tickets/minsk-stambul/` (single hop ✅) |
| `/blog/komandirovka-v-turciyu/` | `301 → /blog/komandirovka-v-turciyu.html` (single hop ✅) |
| `/mobile-preview.html` | `301 → /` (single hop ✅) |
| `/tours/` | `301 → /tickets/` (single hop ✅) |

**No redirect chains or loops** found on spot-checks. `.htaccess` canonicalization (host, trailing-slash blog, minsk-istanbul cannibalization, retired `/tours/`, `/visa-support/`) is clean and single-hop.

---

## Top Priorities

1. **Mobile-preview content & schema parity (High)** — restore FAQPage/BreadcrumbList/Service schema and full body copy to the mobile version, or go responsive. Biggest indexed-content risk under mobile-first.
2. **Normalize NAP (Medium)** — one exact `streetAddress` string sitewide (decide on `оф. 12`); fix mobile-preview's `пр.`/`оф. 12` divergence.
3. **Add security headers (Medium)** — HSTS, X-Frame-Options (or CSP `frame-ancestors`), basic CSP.
4. **Add `sameAs` to TravelAgency schema (Medium)** — strengthen entity/knowledge-graph.
5. **Sitemap `lastmod` realism + minor cleanups (Low)** — real per-file dates; drop the `Host:` line and dead WP disallows from robots.txt; consider deleting the redundant `korporativnye.../index.html` stub.
