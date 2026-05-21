# Content & On-Page SEO Audit — fclass.by

**Date:** 2026-05-21
**Scope:** All public pages — index.html, mobile-preview.html, blog/ (30 articles), tickets/ (15 route pages), service pages (komandirovki, komandirovki-na-vystavki, komandirovochnye-kalkulyator, concierge, cases), resources/ (calculator, dogovor-template), privacy, tours (redirect).
**Method:** Static analysis of committed HTML (= live). Title/meta lengths measured in characters (not bytes).

> Excluded from public-page audit (internal/draft/admin): `web-panel/*`, `questionnaires/*`, `docs/*`, `content/*`, `fclass-landing/*` (staging dupes), `carousels/*`, `firstclass-*.html` (planning docs), `blog/_template.html`.

---

## 0. Top Findings Summary

| # | Severity | Finding |
|---|----------|---------|
| 1 | **Critical** | **Stambul/Istanbul cannibalization** — `tickets/minsk-istanbul/` and `tickets/minsk-stambul/` both target "Авиабилеты Минск — Стамбул 2026" with identical H1; each self-canonicalizes → two pages compete for one query. |
| 2 | **High** | **Суточные cluster cannibalization** — 3 blog posts overlap on "суточные командировка 2026" queries. |
| 3 | **High** | **E-E-A-T weakness** — all blog `author` = `Organization`, no named human expert; only 4/30 posts have a visible byline. Thin author authority for YMYL-adjacent finance/visa content. |
| 4 | **High** | **Banned phrases live** — "корпоративного договора" (organizaciya-komandirovok) and "полный комплект документов" (korporativnye-aviabilety-minsk). |
| 5 | **Medium** | **Money-page interlinking gaps** — 0 blog posts link to `komandirovki-na-vystavki/` or `concierge/`; only 2 link to `komandirovki/`. Those two service pages are near-orphaned from the blog cluster. |
| 6 | **Medium** | **Thin content** — concierge (274w), visa-guide-2026 (283w), komandirovka-v-turciyu (356w), several ticket pages (<450w). |
| 7 | **Medium** | **Mobile content parity** — mobile-preview.html is 465 words vs 819 desktop (-43%); 6 H2 vs 8 desktop. Risk under mobile-first indexing. |
| 8 | **Low** | **3 blog posts missing `dateModified`** (turciyu, organizaciya-komandirovok, strahovka). |
| 9 | **Low** | A few titles >60 chars get truncated in SERP (istanbul 96, komandirovka-v-uzbekistan 65). |

---

## 1. Title Tags

**Method:** char count (Cyrillic counts as 1 char). Optimal 30–60.

### Flagged: >60 chars (truncation risk in SERP)

| Page | Chars | Title |
|------|-------|-------|
| tickets/minsk-istanbul/ | **96** | Авиабилеты Минск — Стамбул 2026: расписание Belavia + Turkish Airlines, цены, виза \| First Class |
| blog/komandirovka-v-uzbekistan-2026 | 65 | Командировка в Узбекистан 2026: что нужно знать белорусу — First Class |
| blog/aviabilety-minsk-stambul | 54 | (OK) |
| blog/komandirovka-v-gruziyu-2026 | 63 | Командировка в Грузию из Беларуси 2026: визы, перелёт, суточные |
| blog/komandirovka-v-turciyu | 64 | Командировка в Турцию: полная поддержка и услуги |
| blog/konsulskiy-sbor-shengen-2026 | 64 | Консульский сбор шенген 2026: сколько платит белорус |
| blog/vizovaya-podderzhka-minsk | 64 | Визовая поддержка в Минске: полный гид на 2026 год — First Class |
| concierge/ | 63 | VIP Консьерж-сервис для командировок — First Class Travel Минск |
| tickets/minsk-sochi/ | 63 | Авиабилеты Минск — Сочи 2026: прямой рейс Belavia \| First Class |

> Only **istanbul (96)** is a hard problem — it will truncate ~40 chars before the brand. The 61–65 range is borderline (Cyrillic renders narrower than Latin in Google's pixel budget, so ~63 chars is usually still safe). **Action:** trim istanbul to ≤60.

### Flagged: <30 chars
- `tours/index.html` (29) — but this is a 0-redirect page (`<meta refresh>` → /tickets/), so not a real concern.

### Duplicate titles
- `index.html` and `mobile-preview.html` share `Авиабилеты и командировки в Минске — авиакасса GDS | First Class`. **Expected** (mobile is a UA-served variant of the same URL), but confirm canonical/handling so both aren't indexed as separate URLs.

### Brand suffix consistency (Low)
Inconsistent separator and brand format: most use `| First Class`, but several use `— First Class` (uzbekistan, konsulskiy-sbor, sutochnye-s-4-aprelya, vizovaya-podderzhka) and some use `First Class Travel Минск` (concierge, blog/index). Standardize to one pattern.

### Keyword stuffing
None flagged. Titles are query-shaped and natural.

---

## 2. Meta Descriptions

**Optimal 70–160 chars.** All audited public pages **have** a meta description except `tours/index.html` (redirect — acceptable).

### Flagged: >160 chars (truncation)
| Page | Chars |
|------|-------|
| index.html / mobile-preview.html | 185 |
| tickets/minsk-istanbul/ | 168 |

### Flagged: <70 chars
| Page | Chars |
|------|-------|
| resources/dogovor-template/ | 101 |
| komandirovochnye-kalkulyator/ | 117 |
- None critically short; lowest is 101. Could be richer but not urgent.

### Duplicate metas
- `index.html` ≡ `mobile-preview.html` (same intent variant). Acceptable; same note as title duplication.

**Verdict:** Meta coverage is strong. Only fix: shorten the index/mobile (185) and istanbul (168) descriptions to ≤160.

---

## 3. H1

- **Every public content page has exactly one H1.** ✅ No missing, no multiple.
- `tours/index.html` has **0 H1** — but it's a redirect stub, acceptable.
- H1s match search intent well (e.g. "Командировка в Грузию из Беларуси 2026: визы, перелёт, суточные").
- **Note:** index.html / mobile H1 ("Авиабилеты для организаций и физлиц") is brand-positioning, not keyword-led. The keyword "авиабилеты Минск" / "командировки" lives in title/subhead. Acceptable for a homepage but the H1 is softer than it could be.

---

## 4. Heading Hierarchy

Checked sequences on representative pages — **no skipped levels** found.
- `blog/komandirovka-v-turciyu`: H1→H2×5→H3→H4×3 (clean).
- `concierge/`: H1→H2→H3×6→H2→H2→H3×3→H4×3 (clean).
- `komandirovki/`: H1→H2×5 with nested H3×21, H4×3 (clean, deep but logical).
- `tickets/minsk-baku/`: H1→H2×7 (flat, fine).

**Verdict:** Hierarchy is healthy across the sample. Low priority.

---

## 5. Thin Content

Body word counts (visible text, scripts/styles stripped). Flag <~300 words.

### Critical / High (thin)
| Page | Words | Severity | Note |
|------|-------|----------|------|
| concierge/ | 274 | High | Money/service page — should be 600+. |
| blog/visa-guide-2026 | 283 | High | Underpowered for "шенгенская виза командировка". |
| blog/komandirovka-v-turciyu | 356 | Medium | Weak vs other country guides (1000–2000w). |
| blog/delovoy-turizm-belarus-2026 | 413 | Medium | |
| blog/strahovka-dlya-komandirovki | 452 | Medium | |
| blog/sutochnye-komandirovki-aprel-2026 | 494 | Medium | Also a cannibalization candidate (§8). |
| privacy/ | 224 | Low | Legal page, acceptable. |

### Thin ticket pages (Medium — route pages should hit 500+ for "авиабилеты Минск — X" intent)
| Page | Words |
|------|-------|
| tickets/minsk-baku/ | 390 |
| tickets/minsk-sharm-el-sheikh/ | 417 |
| tickets/minsk-sochi/ | 416 |
| tickets/minsk-kaliningrad/ | 435 |
| tickets/minsk-erevan/ | 466 |
| resources/calculator/ | 367 |

**Strongest content (good models to clone):** komandirovka-v-polshu (2127w), komandirovka-v-uzbekistan (1884w), korporativnye-aviabilety-minsk (1772w), komandirovka-v-rossiyu (1692w), komandirovki-na-vystavki (1567w).

---

## 6. E-E-A-T Signals

### Strong
- **Trust/legal:** УНП 193582943 present on 37 pages; "с 2018" on 38 pages; Сертификат СА-94 on 3 pages.
- **Dates:** 29/29 blog posts have `datePublished` in JSON-LD; 25/30 have `dateModified`.
- **Schema author:** present on all blog posts.

### Weak (High severity)
- **`author` = `Organization` everywhere** (`{"@type":"Organization","name":"First Class"}`), never a named `Person`. For finance (суточные, нормы Постановление №135) and visa/YMYL-adjacent topics, Google rewards a credentialed human author.
  - **Action:** Add a real `Person` author with bio/role to JSON-LD on at least the finance/visa cluster.
- **Visible bylines on only 4/30 posts.** Most articles have no on-page "Автор / Эксперт" block. Add author byline + short expertise note + dateModified visible.
- **Сертификат СА-94 mentioned on only 3 pages** — surface this trust badge more widely (footer site-wide, ticket pages, service pages).

---

## 7. Internal Linking

| Target money page | # blog posts linking to it |
|-------------------|----------------------------|
| `/tickets/*` | 29 ✅ (excellent) |
| `/komandirovki/` | 2 ⚠️ |
| `/komandirovki-na-vystavki/` | **0** ❌ |
| `/concierge/` | **0** ❌ |

- **tickets/ is well-fed** from the blog — strong internal linking to the primary money funnel.
- **komandirovki-na-vystavki/ and concierge/ are near-orphans** — no inbound links from the 30-article blog cluster. Both are high-value B2B pages. (Medium-High)
  - **Action:** Add contextual links from relevant posts — e.g. `mice-belarus-2026` and `delovoy-turizm-belarus-2026` → komandirovki-na-vystavki; concierge linked from country guides / VIP-relevant posts.
- **komandirovki/** under-linked (only 2). Boost from organizaciya-komandirovok and country guides.
- **CTA consistency:** ticket-page CTAs and forms are consistent ("Подобрать билет Минск — X"); fine.

---

## 8. Keyword / Intent Coverage & Cannibalization Map

### Cannibalization — Critical
**Stambul vs Istanbul ticket pages** (same query "авиабилеты Минск Стамбул 2026"):

| Page | Title | H1 | Words | Canonical |
|------|-------|----|-------|-----------|
| tickets/minsk-istanbul/ | Авиабилеты Минск — Стамбул 2026: расписание Belavia + Turkish Airlines… | Авиабилеты Минск — Стамбул 2026 | 774 | self |
| tickets/minsk-stambul/ | Авиабилеты Минск — Стамбул 2026 | Авиабилеты Минск — Стамбул 2026 | 617 | self |
| blog/aviabilety-minsk-stambul | Минск — Стамбул: гид по авиабилетам 2026 | Авиабилеты Минск — Стамбул 2026: расписание, цены, советы | 1562 | self |

- Two **ticket** pages with identical H1 and self-canonicals = direct internal competition. minsk-istanbul links to minsk-stambul once, but neither defers via canonical.
- **Action:** Pick one canonical winner (istanbul/ is richer: 774w, more H2s, Turkish Airlines + visa + transit hub + юрлица section). 301 or canonical the weaker `minsk-stambul` → `minsk-istanbul`, OR consolidate. The blog `aviabilety-minsk-stambul` (1562w guide) can coexist if it targets informational intent and the ticket page targets transactional — but make the ticket page the canonical commercial target and interlink clearly.

### Cannibalization — High
**Суточные cluster** (overlapping "суточные / нормы 2026" intent):

| Page | Title | H1 | Words | Intended distinct angle? |
|------|-------|----|-------|--------------------------|
| sutochnye-komandirovka-2026 | Суточные за рубежом 2026: нормы и учет | …нормы, расчёт, учёт | 1305 | Evergreen pillar |
| sutochnye-s-4-aprelya-2026 | Новые нормы суточных с 4 апреля 2026 — Беларусь | Новые нормы суточных с 4 апреля 2026 | 818 | News/Постановление №135 |
| sutochnye-komandirovki-aprel-2026 | Суточные командировки: апрель 2026 | …апрель 2026: горячие маршруты | 494 | **Weakest / most redundant** |

- The three overlap heavily on the head term "суточные командировка 2026". `sutochnye-komandirovki-aprel-2026` (494w, thin) is the redundant one.
- **Action:** Designate `sutochnye-komandirovka-2026` as the **pillar**. Fold `sutochnye-komandirovki-aprel-2026` into it (301/canonical) or repurpose it narrowly. Keep `sutochnye-s-4-aprelya-2026` only if it stays a dated news angle that links up to the pillar. Add explicit pillar↔news interlinks.

### Coverage — good
Titles/H1s target clear queries (country guides, route pages, calculators, visa). Strong topical breadth around командировки / авиабилеты / суточные / визы.

---

## 9. Mobile Content Parity (mobile-preview.html)

| Metric | Desktop index.html | mobile-preview.html |
|--------|--------------------|--------------------|
| Body words | 819 | **465 (-43%)** |
| H2 count | 8 | 6 |
| Title / Meta | identical | identical |
| Links to money pages | yes | yes (/tickets/, /blog/, /concierge/) |

- **Medium risk:** Under **mobile-first indexing**, Google indexes the mobile version. The stripped mobile homepage has ~43% less text and 2 fewer sections than desktop. If mobile is served on the same URL by UA sniffing, Google's mobile crawler sees the lighter version → potential loss of homepage content signals.
- **Action:** Bring mobile homepage content/headings to parity with desktop (responsive CSS hiding > content removal), or ensure the canonical/served version Google crawls is the full one. Verify it's not creating a separate indexable URL.

---

## 10. Compliance with Project Rules (Banned Phrases)

| Severity | Page | Issue | Fix |
|----------|------|-------|-----|
| **High** | blog/organizaciya-komandirovok.html (line ~192) | "обсудим условия **корпоративного договора**" | → "договор для юрлиц" |
| **High** | blog/korporativnye-aviabilety-minsk.html | "предоставляет **полный комплект документов** для бухгалтерского учёта" | banned "полный пакет/комплект" pattern → reword (e.g. "согласуем состав закрывающих документов") |

### Cleared (not violations)
- **Fixed discount promises ("скидка 15–25%")** — none found. ✅
- **"корпоративные авиабилеты"** as a banned offer phrase — not used; the page H1 correctly reads "Договор на авиабилеты для юрлиц". ✅ (Other "корпоратив*" usages are descriptive — "корпоративные тарифы", "корпоративная карта сотрудника", "корпоративные мероприятия" — not the banned договор/билеты offer wording.)
- **"закрывающих документов"** alone (with "пакет/состав/согласуем") — widespread but **not** the banned "полный пакет/комплект закрывающих документов" exact phrase. Acceptable as written. (Only the two High items above cross the line.)
- **Tourism wording on business pages** — `komandirovki/`, `komandirovki-na-vystavki/`, `concierge/` contain "тур/путешеств" but in compliant context: "не туристическая поездка, а инвестиция", "бизнес-путешествий", "частные и туристические поездки" (scope statement). No misframing of business trips as tourism. ✅ (Low — monitor.)

---

## Priority Action List

1. **[Critical]** Resolve Stambul/Istanbul ticket-page cannibalization — canonical the weaker `minsk-stambul` → `minsk-istanbul`.
2. **[High]** Fix 2 banned phrases (organizaciya-komandirovok, korporativnye-aviabilety-minsk).
3. **[High]** Consolidate суточные cluster — fold thin aprel-2026 into the pillar.
4. **[High]** Add named `Person` authors + visible bylines (start with finance/visa cluster).
5. **[Medium]** Add internal links to orphaned `komandirovki-na-vystavki/` & `concierge/`; boost `komandirovki/`.
6. **[Medium]** Expand thin pages: concierge (274w), visa-guide-2026 (283w), turciyu (356w), thin ticket pages.
7. **[Medium]** Achieve mobile homepage content parity (465→~819w).
8. **[Low]** Trim istanbul title (96→≤60) and index/istanbul meta (≤160); add `dateModified` to 3 posts; standardize brand suffix.
