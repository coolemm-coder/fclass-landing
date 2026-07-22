# Cabinet audit - Yandex and Google

Date: 2026-07-21
Site: fclass.by
Mode: read-only browser audit of connected dashboards.

## Yandex Metrica

Counter: `107237229`, site: `fclass.by`.

List view, last 24 hours:

- Visits: 66
- Pageviews: 89
- Visitors: 64
- Goal `Заявка`: 0

Overview, yesterday 2026-07-20:

- Visits: 77, +185.19%
- Pageviews: 94, +184.85%
- Visitors: 74, +196%
- Avg time on site: 1m 22s, +256.85%
- Page depth: 1.22
- Bounce rate: 23.38%

Overview, month 2026-06-22 to 2026-07-21:

- Visits: 1,490, +24.69%
- Pageviews: 1,818, +23.42%
- Visitors: 1,292, +25.07%
- Avg time on site: 1m 03s, -20.04%
- Page depth: 1.22
- Bounce rate: 23.62%

Traffic sources, month:

- Search engines: 1,252 visits, 83.97%; 1,074 visitors; bounce 14.30%
- Direct: 127 visits, 8.52%; bounce 53.54%
- Referral: 107 visits, 7.18%; bounce 95.33%
- Internal: 4 visits
- Social: 1 visit

Top pageviews, month:

- `/komandirovochnye-kalkulyator/`: 495 pageviews
- `/blog/komandirovka-v-rossiyu-2026.html`: 326
- `/`: 224
- `/blog/sutochnye-komandirovka-2026.html`: 224
- `/blog/pryamye-reysy-iz-minska-2026.html`: 57
- `/tickets/direct-flights/`: 56
- `/blog/konsulskiy-sbor-shengen-2026.html`: 53

Top landing pages, month:

- `/komandirovochnye-kalkulyator/`: 442 visits
- `/blog/komandirovka-v-rossiyu-2026.html`: 282
- `/`: 194
- `/blog/sutochnye-komandirovka-2026.html`: 177
- `/blog/pryamye-reysy-iz-minska-2026.html`: 54

Goals, month:

- `LEAD / Заявка`: 3 visits
- `PHONE_CLICK / Клик на телефон`: 0 visits
- Auto goal `переход в мессенджер`: 11 visits
- Auto goal `отправка формы`: 10 visits
- Auto goal `клик по номеру телефона`: 2 visits
- Auto goal `отправка формы заявки`: 7 visits
- Auto goal `отправил контактные данные`: 7 visits
- Auto goal `заполнил контактные данные`: 7 visits

Audit notes:

- Metrica confirms organic information traffic, not enough commercial traffic.
- Page depth 1.22 means users mostly consume one page and leave.
- Goals are fragmented: manual `LEAD`, manual `PHONE_CLICK`, and auto goals overlap. Reporting should be unified into a small set of business goals: Telegram lead, phone lead, form lead, email lead, tariff/pricing intent.
- The manual phone goal is not firing while auto phone clicks fire, which points to event mismatch.

## Yandex Webmaster

Site list:

- State: no problems detected
- IKS: 10
- Pages added: 132, +1%
- Pages in search: 62, +2%
- Crawl by Metrica counters: enabled

Dashboard:

- Diagnostics: no errors/recommendations.
- Duplicate titles: 0.
- Duplicate descriptions: 2 pages.
- Search clicks block showed 13 clicks and -56.67% for the dashboard period.
- Recent search updates: 2026-07-14 to 2026-07-21, 1 page added, 0 removed.
- Crawl history 2026-06-22 to 2026-07-19: 16 URLs with HTTP 2xx, 0 URLs with 3xx, 0 URLs with 4xx in the summary block.

Duplicate descriptions:

- Duplicate description text: `Сайт по продаже авиабилетов`
- `/services/`, crawled 2026-01-30
- `/calendar/`, crawled 2025-09-20

Top Yandex queries visible on dashboard:

- `консульский сбор для белорусов 2026`: 68 impressions, 27 clicks
- `командировочные в беларуси в 2026 году`: 150 impressions, 14 clicks
- `нужна ли виза в казахстан для белорусов`: 61 impressions, 7 clicks
- `командировочные в беларуси в 2026`: 54 impressions, 5 clicks
- `консульский сбор для белорусов`: 54 impressions, 5 clicks
- `оплата командировочных в беларуси в 2026 году`: 27 impressions, 5 clicks
- `командировочные расходы в беларуси в 2026 году`: 184 impressions, 5 clicks
- `прямые рейсы из минска в какие страны`: 59 impressions, 5 clicks

Audit notes:

- Yandex indexation is not broken, but only 62 pages are in search out of 132 added.
- Visible clicks are dominated by informational queries, not transactional aviation/B2B queries.
- `/services/` and `/calendar/` are old low-quality index artifacts and should be fixed or redirected.

## Yandex Business

Profile: `Первый класс`, address shown as `Минск, проспект Победителей, 11`.

Observed:

- Rating: 5.0.
- Profile state: not filled.
- Checklist asks to verify/update: working hours, website, phone.
- Media: only 1 photo/video; Yandex asks for at least 3.
- Reviews section shows 7 items/unread in navigation.
- Recent reviews are mostly about tours, hotels and holidays.
- Visible weekly stats: phone clicks 2, website clicks 3, route builds 0.

Audit notes:

- Local profile is underfilled; this is a GEO visibility problem.
- Review content conflicts with current positioning: site is now focused on business trips and tickets, while reviews still heavily mention tours/rest.
- Need request new reviews specifically about business trips, tickets, invoices, visas, and manager support.

## Google Search Console

Property: `https://fclass.by/`.

Overview:

- Total web search clicks: 1,017.
- Indexed pages: 47.
- Not indexed pages: 28,612.
- Core Web Vitals: 13 good mobile URLs; desktop has no data in overview.
- HTTPS: 13 HTTPS, 0 non-HTTPS.
- Breadcrumbs: 10 valid, 0 invalid.

Performance, web search, 2026-04-20 to 2026-07-19:

- Clicks: 1,017.
- Impressions: 24,154.
- CTR: 4.2%.
- Average position: 7.6.

Top queries:

- `командировочные в рф из рб 2026`: 54 clicks, 370 impressions
- `командировочные рб 2026`: 43 clicks, 1,175 impressions
- `суточные рб 2026`: 23 clicks, 1,059 impressions
- `суточные в рф из рб 2026`: 18 clicks, 95 impressions
- `суточные рб 2026 за границу`: 16 clicks, 202 impressions
- `командировочные рб`: 12 clicks, 477 impressions
- `нормы командировочных расходов за границу рб 2026`: 10 clicks, 172 impressions
- `командировочные в москву из рб 2026`: 9 clicks, 82 impressions

Top pages:

- `/komandirovochnye-kalkulyator/`: 346 clicks, 9,231 impressions
- `/blog/komandirovka-v-rossiyu-2026.html`: 268 clicks, 3,390 impressions
- `/blog/sutochnye-komandirovka-2026.html`: 244 clicks, 7,203 impressions
- `/`: 81 clicks, 550 impressions
- `/blog/komandirovka-v-kazahstan-2026.html`: 17 clicks, 332 impressions
- `/blog/pryamye-reysy-iz-minska-2026.html`: 15 clicks, 1,642 impressions
- `/tickets/aviabilety-dlya-yurlic/`: 8 clicks, 551 impressions

Indexing:

- Sitemap `/sitemap.xml`: successful.
- Submitted 2026-06-01; last processed 2026-07-20.
- Discovered pages: 56.
- Not indexed reasons:
  - 404: 20,387 URLs
  - 403: 1,525 URLs
  - blocked by robots.txt: 706 URLs
  - redirect pages: 21
  - server error 5xx: 11
  - soft 404: 8
  - alternate page with canonical: 8
  - duplicate, Google chose canonical not selected by user: 2
  - redirect error: 1
  - noindex: 1

Audit notes:

- Sitemap is OK; index bloat comes from historic/discovered garbage URLs, not from submitted sitemap.
- Google commercial visibility is weak: the main B2B ticket page has 8 clicks in 3 months.
- Google already ranks informational pages well; the issue is conversion path and commercial page authority.

## Google Analytics 4

Property selected: `fclass.by`, account area `LandingPro.by`.

Home, last 7 days:

- Active users: 296, +8.4%.
- Events: 1.4k, +7.2%.
- Key events: 0.
- New users: 284, +8.4%.
- Active users in last 30 min: 1.

Traffic, last 7 days:

- Sessions: Organic Search 331, Direct 31, Referral 5, Organic Social 1.
- First user source/medium: google / organic 153; yandex.by / referral 67; yandex.ru / referral 36; direct 26; ya.ru / referral 5.

Events, last 7 days:

- `page_view`: 415
- `session_start`: 370
- `first_visit`: 284
- `user_engagement`: 268
- `scroll`: 47
- `click`: 3
- `form_start`: 4

GA recommendations:

- GA shows recommendation to link Search Console property `https://fclass.by/`.

Audit notes:

- GA4 is not conversion-ready: key events are 0.
- Search Console is not linked to GA4, so GA cannot show query/landing-page behavior together with conversions.
- Current GA events are mostly default events; business lead events are not configured as key events.

## Google Business Profile

Locations view:

- `LandingPro`: verified.
- `ООО Первый класс`: status `Требуется подтверждение`.
- Address shown: `победителей 11 12, минск, город Минск, Беларусь`.

Audit notes:

- Google local profile for First Class is not verified. This is a major GEO/local SEO blocker.
- Address format should be checked: `победителей 11 12` looks like office/building formatting, not a polished address.

## Priority Recommendations

1. Fix measurement first.
   - In GA4 create/mark key events for Telegram lead, phone click, form submit, email click, tariff click.
   - Link Google Search Console to GA4.
   - In Yandex Metrica consolidate goals and ensure site events use the same identifiers.

2. Fix local GEO.
   - Verify Google Business Profile for `ООО Первый класс`.
   - Complete Yandex Business checklist: hours, website, phone, at least 3 photos/videos.
   - Add B2B/business-trip oriented photos and review requests.
   - Reply to unread Yandex reviews.

3. Clean old index artifacts.
   - Fix or redirect `/services/` and `/calendar/`.
   - Investigate Google 404/403 clusters; likely old spam/discovered URLs and server protection artifacts.
   - Keep sitemap clean and submit updated sitemap after major structure changes.

4. Move SEO traffic toward money pages.
   - Add stronger internal CTAs from calculator and top blog pages to `/komandirovki/`, `/tickets/aviabilety-dlya-yurlic/`, `/tarify/`, `/visa-support/`.
   - Build commercial landing clusters for: business trip booking, airfare by invoice, flights for legal entities, routes from Minsk, visa support for business trips.
   - Use informational winners as feeders, not as dead-end pages.

5. Lead diagnosis.
   - Current traffic is not the main problem. Conversion and commercial intent are.
   - With 1,490 monthly visits and only 3 manual LEAD visits, the effective lead conversion is around 0.2% for the main goal.
   - Messenger/form auto goals show some interest, but tracking fragmentation makes lead accounting unreliable.

## Implemented After Audit

Codex changes made after the cabinet audit:

- Added `assets/lead-tracking.js`.
  - Delegated tracking for phone, email, Telegram, WhatsApp, tariff links, commercial page links and form submit intent.
  - Sends semantic GA4 events: `lead_phone_click`, `lead_email_click`, `lead_messenger_click`, `pricing_intent`, `commercial_intent`, `lead_form_submit_intent`.
  - Sends Yandex goals: `PHONE_CLICK`, `EMAIL_CLICK`, `MESSENGER_CLICK`, `TARIFF_CLICK`, `COMMERCIAL_INTENT`, `FORM_SUBMIT_INTENT`.
  - Phone/email/messenger clicks also send Yandex `LEAD` and GA4 `generate_lead` as lead intent.

- Connected `assets/lead-tracking.js` on priority pages:
  - `/`
  - `/komandirovochnye-kalkulyator/`
  - `/blog/komandirovka-v-rossiyu-2026.html`
  - `/blog/sutochnye-komandirovka-2026.html`
  - `/komandirovki/`
  - `/tickets/`
  - `/tickets/aviabilety-dlya-yurlic/`
  - `/tarify/`
  - `/visa-support/`
  - `/resources/calculator/`

- Added commercial internal links from top informational traffic pages:
  - Calculator page now links directly to `/komandirovki/`, `/tickets/aviabilety-dlya-yurlic/`, `/tarify/`.
  - Russia business-trip guide now links to airfare by invoice, full business-trip organization and tariffs.
  - Per-diem/expenses guide now links to business-trip organization, airfare by invoice and tariffs.

- Cleaned wording in repeated messenger CTA blocks:
  - Removed over-specific `счёт-фактура` wording.
  - Replaced with safer `договор, счёт, акт и маршрутные квитанции`.

- Added 301 redirects for old Yandex Webmaster duplicate-description URLs:
  - `/services/` -> `/komandirovki/`
  - `/calendar/` -> `/resources/calculator/`

Account-side actions still not changed by Codex because they modify external accounts:

- Mark GA4 events as key events.
- Link GA4 with Google Search Console.
- Verify Google Business Profile for `ООО Первый класс`.
- Complete Yandex Business profile fields/photos/hours and reply to reviews.

## Visual CTA Simplification Draft

Codex local draft after user feedback that the lower CTA block felt too heavy:

- Replaced the repeated dark bottom messenger CTA on:
  - `/komandirovochnye-kalkulyator/`
  - `/blog/komandirovka-v-rossiyu-2026.html`
  - `/blog/sutochnye-komandirovka-2026.html`
- New component is a compact light strip:
  - white background;
  - thin gold left border;
  - title `Нужна помощь с поездкой?`;
  - short practical text;
  - two calm actions: `Telegram` and `Позвонить`.
- Removed the floating WhatsApp button from the home page draft; left one Telegram bot floating action with an accessible label.
- This draft is intentionally calmer and more B2B/professional than the previous dark promotional messenger block.

## Mobile Footer Compacting

Codex follow-up after user clarified that the problem was the very bottom footer on mobile, not the CTA strip above it:

- Updated home page footer in `index.html`.
- Desktop footer remains complete with all columns and certificate links.
- Mobile footer now hides the long stacked footer columns and certificate strip at `max-width: 768px`.
- Added compact mobile-only footer links: tickets, business trips, legal entities, tariffs.
- Added mobile-only direct phone and email rows.
- Replaced the incorrect `footer-links` class on the privacy-policy inline link with a dedicated `footer-policy-link`.
- Mobile sticky CTA (`Позвонить / Telegram`) now hides when the footer is visible, so it does not cover the legal/footer area.
- Goal: reduce footer length on phones while keeping the key navigation and contact paths reachable.
