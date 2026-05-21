# fclass.by — GEO (AI-search) + Images + Mobile Audit

**Date:** 2026-05-21
**Scope:** llms.txt, AI-crawler access, citability/GEO, brand/entity signals, images, mobile-preview.html
**Live:** https://fclass.by · **Local source:** `/Users/admin/Desktop/FirstClass_Automation/`

> Note on source-of-truth: the **live** `https://fclass.by/llms.txt` (200) is richer and newer (updated 2026-05-19) than the local repo copy `llms.txt` (dated 2026-05-20 in mtime but shorter content). This audit assesses the **live** version. Sync the repo copy to match the deployed file.

---

## Executive scorecard

| Area | Grade | Worst severity |
|---|---|---|
| llms.txt | A- (strong) | Low |
| AI crawler access | B (works, gaps) | Medium |
| Citability / GEO | B+ | Medium |
| Brand / entity signals | C+ | High |
| Images | B | Medium |
| Mobile version (UA-sniff) | C | High |

---

## 1. llms.txt — Quality assessment

**Verdict: strong, above industry average.** Returns 200, well-formed Markdown, follows the llms.txt spec (H1 title + blockquote summary + sectioned link lists with descriptions).

What it does well:
- Clear H1 + one-paragraph business summary an LLM can quote verbatim.
- "Ключевые факты" block: location, specialization, Belavia accreditation, since-2018, IG follower count, last-updated date — exactly the quotable atoms AI engines lift.
- Logical sections: B2B services, core resources, programmatic route pages, blog cluster, current blog, **and a standout "Авиа-санкции и ограничения 2026" block** (EU airspace closure, no Belavia to EU, transit-only routing). That sanctions block is genuinely high-value for AI answers about "flights from Minsk" and is the kind of factual, current, non-obvious content AI engines reward.
- Full contact block (site, phone, email, IG handle, Telegram bot).

Improvements (Low severity):
- **(Low)** No `## Optional` / secondary section — spec allows a deprioritized bucket; minor.
- **(Low)** IG follower count "18,800+" is a soft, decaying claim — fine in llms.txt but date-stamp it or generalize ("18K+").
- **(Low)** Add a one-line canonical entity statement near top: "First Class — торговая марка [юрлицо/УНП], аккредитованный агент Belavia." LLMs use this for entity disambiguation.
- **(Low)** Two links point to the same URL with different labels (`aviabilety-dlya-yurlic/` listed twice as "по безналу" and "по договору"). Dedupe or differentiate.
- **(Medium — cross-cutting)** Some llms.txt URLs reference pages that should be verified live (e.g. `/resources/calculator/`, `/resources/dogovor-template/`, `/cases/`, `/visa-support/` which `.htaccess` 301-redirects to a blog post). A dead/redirecting link in llms.txt erodes trust signals. **Verify every llms.txt URL returns 200** (note `/visa-support/` is a 301 → use the final blog URL in llms.txt).

---

## 2. AI crawler access (robots.txt)

Live robots.txt has explicit `Allow: /` blocks for several AI agents. Status by requested crawler:

| Crawler | Purpose | Status | Severity |
|---|---|---|---|
| **GPTBot** (OpenAI training) | ✅ Explicit `Allow: /` | OK | — |
| **ChatGPT-User** (ChatGPT browsing) | ✅ Explicit `Allow: /` | OK | — |
| **ClaudeBot** (Anthropic) | ✅ Explicit `Allow: /` | OK | — |
| **PerplexityBot** | ✅ Explicit `Allow: /` | OK | — |
| **Google-Extended** (Gemini/AI training) | ✅ Explicit `Allow: /` | OK | — |
| **OAI-SearchBot** (OpenAI search index) | ⚠️ Not named → falls under `User-agent: *` (allowed) | Implicit allow | Low |
| **anthropic-ai** (legacy Anthropic UA) | ⚠️ Not named → `*` allow | Implicit allow | Low |
| **YandexGPT / YandexAdditional** | ⚠️ Not named → `*` allow | Implicit allow | **Medium** |
| **CCBot** (Common Crawl — feeds many LLMs) | ⚠️ Not named → `*` allow | Implicit allow | **Medium** |

Findings:
- **(Good)** No AI crawler is blocked. The named bots are all explicitly welcomed.
- **(Medium)** `Crawl-delay: 1` is set only in the `*` group, **not** in the per-AI-bot groups. Because robots.txt is "most-specific group wins," GPTBot/ClaudeBot/etc. match their own named group and **ignore the `*` group entirely** — meaning they also **ignore all the `Disallow:` rules** (`/api/`, `/wp-admin/`, legacy Bitrix paths, `*.php`, query traps). Result: AI bots are allowed to crawl paths you intended to hide. **Fix:** add the same `Disallow:` lines (or at least the sensitive ones) to each AI-bot group, or rely on `.htaccess` 410/Gone (already done for `/api/`, `/docs/` etc., so impact is limited — but blog/legacy traps are not all hard-blocked).
- **(Medium)** CCBot and YandexGPT not named. Given the Belarus/RU market, explicitly add `YandexAdditional` (Yandex's AI/Neuro crawler) and `CCBot` groups with `Allow: /` for completeness, or accept the `*` default. Decide intentionally rather than by omission.
- **(Low)** `Host:` directive is non-standard/deprecated; harmless.

---

## 3. Citability / GEO (passage-level)

AI engines cite pages that have **direct-answer passages, tables, definitions, and dated facts.** Page-by-page:

| Page | Tables | H2/H3 | FAQ schema | Citability |
|---|---|---|---|---|
| `komandirovki-na-vystavki/` | **7 tables** | 7 / 9 | — | **Strong** — table-heavy, very quotable |
| `komandirovki/` | **0 tables** | 5 / 21 | ✅ 6-Q FAQPage | Medium — good FAQ but no comparison tables |
| `blog/komandirovki-belarus-2026.html` | 2 | 8 / 11 | ✅ (3 ld+json) | Strong — dated fact "суточные 13 BYN/день с 04.04.2026" is exactly what AI lifts |
| `blog/komandirovka-v-rossiyu-2026.html` | 3 | 8 / 18 | ✅ (3 ld+json) | Strong |
| `blog/korporativnye-aviabilety-minsk.html` | 3 | 10 / 14 | ✅ (3 ld+json) | Strong |
| `index.html` | 0 | 8 / 11 | ✅ 15-Q FAQ + Service + TravelAgency + Breadcrumb | Strong (schema), Medium (prose) |

Findings:
- **(Strong)** Blog cluster is well-built for GEO: dated regulatory facts (suточные, ЭСЧФ, НДС, валютный контроль), comparison tables, FAQPage schema on every article. This is the right pattern.
- **(Medium)** `komandirovki/` (the primary B2B landing and a money page) has **zero tables**. Add 1–2 comparison/checklist tables (e.g. "что входит в командировку", "документы для бухгалтерии: документ → назначение") to convert it into a citable answer for "что входит в организацию командировки".
- **(Low)** Consider adding a short definition block ("Служебная командировка — это…") near the top of hub pages; definition passages get cited heavily by AI Overviews.
- **(Strong)** llms.txt sanctions block + dated suточные fact give the site authoritative, current answers competitors likely lack.

---

## 4. Brand / entity signals

| Signal | Status | Severity |
|---|---|---|
| Organization/TravelAgency schema on home | ✅ Present (rich: address, geo, hours, aggregateRating, OfferCatalog) | — |
| **`sameAs` (social/entity links)** | ❌ **MISSING** on the TravelAgency node | **High** |
| Consistent NAP | ⚠️ **Inconsistent** (see below) | **High** |
| Logo in schema (`"logo"`) | ❌ Missing `logo` and `image` properties | Medium |
| `contactPoint` | ❌ Missing (only flat `telephone`) | Low |
| "About"/entity-establishing presence | ⚠️ Partial (expertise section + about-bg, no dedicated /about) | Medium |

Findings:
- **(High) No `sameAs`.** The TravelAgency schema has no `sameAs` array linking Instagram (@firstclass.travel.by), the Telegram bot, or any directory/Wikipedia/2GIS/Yandex profile. `sameAs` is the single most important signal for entity consolidation in Google Knowledge Graph + AI engines. The page links to Telegram/IG in HTML but the **machine-readable entity graph doesn't connect them.** Add:
  ```json
  "sameAs": [
    "https://www.instagram.com/firstclass.travel.by/",
    "https://t.me/fclassmsk_bot"
  ]
  ```
  (Add Yandex Business / 2GIS / Google Business profile URLs too once available — high impact for BY local + AI entity matching.)
- **(High) NAP inconsistency between desktop and mobile schema:**
  - Desktop `index.html`: `"streetAddress": "просп. Победителей, 11"`, geo `53.909249 / 27.548248`
  - Mobile `mobile-preview.html`: `"streetAddress": "пр. Победителей, 11, оф. 12"`, geo `53.9092 / 27.5482`
  - `komandirovki-na-vystavki/`: `"просп. Победителей, 11"`
  - Conflicting street-address strings ("просп." vs "пр.", with/without "оф. 12") and differing geo precision for the same business hurt entity confidence. **Standardize one canonical NAP string** across all schema blocks and llms.txt.
- **(Medium)** Add `"logo"` and `"image"` to the TravelAgency node (point to `https://fclass.by/logo.png`). Required for rich-result/knowledge-panel eligibility.
- **(Medium)** No dedicated `/about/` (entity) page; the home "expertise" section partly covers it. A thin About page with founding story, legal entity name + УНП, accreditation, and team strengthens E-E-A-T and gives AI a canonical "about this org" target.

---

## 5. Images

Overall positive: **all `<img>` across audited pages carry meaningful alt text** (0 missing/empty alt on content images; the Yandex Metrika tracking pixel has empty alt, which is correct). Hero uses `<picture>` + WebP + `loading="eager"` + `fetchpriority="high"`.

| Page | Imgs | Alt coverage | WebP `<picture>` | width/height | lazy |
|---|---|---|---|---|---|
| `index.html` | 5 | 5/5 ✅ | 2 (hero, about) ✅ | **0/5 ❌** | about + footer logo ✅ |
| `komandirovki/` | 3 | 3/3 ✅ | 0 ❌ (hero is raw `/hero-bg.jpg`) | 0/3 ❌ | not on hero |
| `komandirovki-na-vystavki/` | 2 | 2/2 ✅ | 0 (logos only) | 0/2 ❌ | — |
| `blog/komandirovki-belarus-2026.html` | 2 | 2/2 ✅ | 0 | 0/2 ❌ | — |
| `mobile-preview.html` | 3 logos + pixel | ✅ | 0 | 0 ❌ | — |

Findings:
- **(Medium — CLS risk) No `<img>` anywhere has explicit `width`/`height` attributes.** This is the top image issue. Without intrinsic dimensions the browser can't reserve space → layout shift (CLS), penalized in Core Web Vitals and a known AI/Google quality factor. **Add `width`/`height` (or CSS `aspect-ratio`) to every img**, especially the hero and about images.
- **(Medium — worst page: `komandirovki/`)** Hero is a raw `<img src="/hero-bg.jpg">` — no `<picture>`/WebP, no `loading`, no dimensions. The home page does this correctly (WebP + eager + fetchpriority); sub-pages don't. Bring the optimized hero pattern to `komandirovki/` and other landing pages.
- **(Low)** `hero-bg.jpg` is 553 KB and `about-bg.jpg` 529 KB on disk; WebP variants (299 KB / 281 KB) exist and are served via `<picture>` on home — good. Ensure WebP is the primary delivered format everywhere and consider AVIF for further savings. OG image still points to `.jpg` (fine for social).
- **(Low)** `og:image` is `hero-bg.jpg` (553 KB) — large for a social preview; a dedicated 1200×630 optimized OG image would be faster.

---

## 6. Mobile version deep-dive (`mobile-preview.html`)

Served to mobile UA at `/` via `.htaccess` UA-sniff (URL stays `/`, file kept private — direct hits to `/mobile-preview.html` 301 → `/`).

### 6a. Content parity vs desktop
| | Mobile | Desktop |
|---|---|---|
| H1 | 1 | 1 |
| H2 | 6 | 8 |
| H3 | 3 | 11 |
| Sections | 9 | 12 |
| File size | 55 KB | 141 KB |
| Schema (ld+json) | **1** | **4** |

- **(High) Content is stripped down (~40% of desktop).** Fewer H2/H3, fewer sections, and **only 1 schema block** (TravelAgency) vs desktop's 4 (TravelAgency + 15-Q FAQPage + Service + BreadcrumbList). Under **mobile-first indexing, Google indexes the MOBILE version** — so the missing FAQPage/Service/Breadcrumb schema and reduced content are what actually gets indexed. The rich FAQ schema on desktop is effectively invisible to Google. **This is the core SEO risk of this setup.**

### 6b. Mobile UX — generally good
- ✅ `viewport` meta present (`width=device-width, initial-scale=1.0`).
- ✅ Sticky bottom CTA (`.sticky-cta`, `min-height:44px`, safe-area-inset padding).
- ✅ Tap targets are healthy: buttons `min-height:52px`, drawer links 48px, nav call button 42px (44px is the guideline — nudge the 42px to 44px+).
- ✅ Floating social button, slide-out drawer, `env(safe-area-inset-bottom)` handled.
- ✅ Body fonts 14–16px; the 10–11px sizes are limited to eyebrows/labels/chips (acceptable convention).
- ⚠️ No hero image on mobile (logo-only header) — fine for speed, but loses a brand/visual signal vs desktop.

### 6c. Own title/meta/canonical/schema
- ✅ Has its own `<title>` (same as desktop — good), `meta description` (identical), `keywords`, `author`, `robots: index,follow`, verification tags, OG + Twitter cards.
- ✅ **`<link rel="canonical" href="https://fclass.by/">`** — correctly canonicalizes to the root, NOT to itself or `mobile-preview.html`. (Requested check #7: confirmed.)
- ⚠️ Has TravelAgency schema but with the **conflicting NAP** ("пр. Победителей, 11, оф. 12") flagged in §4 — and **lacks** the FAQ/Service/Breadcrumb schema present on desktop.

### 6d. SEO risk of UA-sniffing (separate-file, no separate URL)
**(High) — Architectural risk.** Serving a different HTML file by User-Agent at the same URL is **cloaking-adjacent and against mobile-first best practice:**
1. **Mobile-first indexing penalty:** Googlebot crawls as a mobile UA → it receives `mobile-preview.html`, the **stripped** version. Desktop's richer content + 3 extra schema blocks are NOT what Google indexes. You're indexing your weaker page.
2. **Cloaking perception:** UA-based content swapping at one URL is exactly the pattern Google warns about. Risk is real if mobile/desktop diverge in content (they do here).
3. **Parity drift / maintenance:** Two HTML files must be hand-synced (title, schema, NAP already drifted — see §4). Every content/schema change must be made twice.
4. **No `Vary: User-Agent` header** observed — caches/CDNs may serve the wrong variant to the wrong device.

**Recommendation (High priority):** **Migrate to a single responsive page** (one `index.html` with CSS media queries / responsive layout). This is Google's explicitly recommended config and eliminates parity drift, the cloaking risk, and the mobile-first-indexing content gap in one move. If a full responsive rebuild isn't immediate:
- **Short term:** bring mobile-preview.html to **full content + schema parity** with desktop (port the FAQPage, Service, BreadcrumbList schema; fix NAP to the canonical string), and add `Vary: User-Agent` to the mobile rewrite response.
- **Medium term:** consolidate to responsive.

### 6e. Mobile-preview indexing exposure (good)
- `mobile-preview.html` is **NOT in `sitemap.xml`** and **NOT internally linked** anywhere — so it won't be discovered as a standalone duplicate URL. Combined with the 301 on direct hits and the self-canonical to `/`, the duplicate-URL exposure is well contained. The remaining risk is purely the mobile-first-indexing content gap, not duplicate URLs.

---

## Prioritized fix list

**Critical:** none.

**High**
1. Add `sameAs` (IG, Telegram, + Yandex/2GIS/Google Business when available) to TravelAgency schema. (§4)
2. Standardize NAP across desktop/mobile/sub-page schema + llms.txt — one canonical address string + consistent geo. (§4)
3. Resolve mobile-first-indexing gap: migrate to responsive OR bring `mobile-preview.html` to full content + schema parity with desktop. (§6a, §6d)

**Medium**
4. Add `width`/`height` (or `aspect-ratio`) to all `<img>` to prevent CLS. (§5)
5. Add `Disallow:` rules (sensitive paths) to each named AI-bot group in robots.txt — they currently ignore all `*` Disallows. (§2)
6. Apply WebP `<picture>` + `loading`/`fetchpriority` hero pattern to `komandirovki/` and other sub-page heroes. (§5)
7. Add `logo`/`image` to TravelAgency schema; verify every llms.txt URL returns 200 (fix `/visa-support/` 301). (§4, §1)
8. Add comparison/checklist tables to `komandirovki/` for citability. (§3)
9. Explicitly decide YandexGPT/CCBot crawler policy. (§2)

**Low**
10. Sync repo `llms.txt` to live; date-stamp/soften IG follower claim; dedupe duplicate yurlic links. (§1)
11. Bump 42px nav-call tap target to ≥44px. (§6b)
12. Consider dedicated `/about/` entity page; smaller dedicated OG image. (§4, §5)
