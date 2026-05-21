# ACTION-PLAN — fclass.by SEO (2026-05-21)

Приоритеты: **Critical** (сразу) > **High** (неделя) > **Medium** (месяц) > **Low** (бэклог).
Health Score сейчас: **74/100**. Закрытие Critical+High → ориентировочно **85+**.

---

## 🔴 CRITICAL — сделать сразу

### C0. Вернуть money-страницы в индекс Google (добавлено по live-данным GSC 21.05)
**Проблема:** `/tickets/aviabilety-dlya-yurlic/` = «Discovered — not indexed» (краулилась НИКОГДА); `/tickets/minsk-batumi/`, `/blog/aviabilety-dlya-yur-lic.html` = «unknown to Google». Коммерческих страниц нет в выдаче Google → ~0 коммерческого трафика. Причина: краул-голод (ИКС=10) + страницы-сироты. Детали: `LIVE-DATA-INDEXATION-2026-05-21.md`.
**Действия:** (1) Яндекс «Переобход» money-URL (квота 139/150 свободна); (2) GSC «Запросить индексирование»; (3) перелинковка = усиленный H5 (без неё Google снова выкинет сирот); (4) `/blog/aviabilety-dlya-yur-lic.html` → canonical/301 на `/tickets/aviabilety-dlya-yurlic/`; (5) удалить 2 битых sitemap в GSC.
**Effort:** 1-2ч + ждать переобход.

### C1. Решить mobile-first провал (главное)
**Проблема:** `mobile-preview.html` отдаётся мобильным UA, но содержит ~40% контента и 1/4 schema. Google/Яндекс индексируют его. Яндекс: `NOT_MOBILE_FRIENDLY`.
**Варианты:**
- **(A, правильно)** Перейти на **единый адаптивный** `index.html` (responsive), убрать UA-sniffing из `.htaccess`. Десктопный index.html уже адаптивный (есть @media) — проверить мобильную вёрстку и отключить подмену.
- **(B, быстро)** Довести `mobile-preview.html` до **полного паритета**: все 4 schema-блока (FAQPage, Service, BreadcrumbList + TravelAgency), весь контент/H2, те же ссылки. + добавить `Vary: User-Agent` в заголовки.
**Рекомендация:** A в перспективе, B — сейчас как hotfix.
**Effort:** A — 4-6ч, B — 2-3ч.

### C2. Снять каннибализацию Стамбул
301-редирект (или canonical) `tickets/minsk-stambul/` → `tickets/minsk-istanbul/` (istanbul богаче: 774 сл., +Turkish, виза, транзит, юрлица). В `.htaccess` уже есть подобные 301 — добавить правило.
**Effort:** 15 мин.

---

## 🟠 HIGH — в течение недели

### H1. Свести «суточные»-кластер
Свернуть `sutochnye-komandirovki-aprel-2026` (494 сл., тонкий) в pillar `sutochnye-komandirovka-2026` (1305 сл.) → 301. `sutochnye-s-4-aprelya-2026` оставить как news, добавить canonical/ссылку на pillar.
**Effort:** 30 мин.

### H2. Убрать 2 запрещённые фразы
- `blog/organizaciya-komandirovok.html`: «корпоративного договора» → «договора для юрлиц».
- `blog/korporativnye-aviabilety-minsk.html`: «полный комплект документов» → «состав документов согласуем до оплаты».
**Effort:** 10 мин.

### H3. Усилить E-E-A-T (YMYL-кластер: суточные, визы)
- Добавить именного автора (Author schema + видимая подпись «Эксперт по командировкам, First Class») на финансово-визовые посты.
- Добавить блок «Источники» (НБРБ, Минфин, постановления) где уместно.
**Effort:** 2-3ч.

### H4. Добавить sameAs + logo + image в schema
В Organization/TravelAgency: `sameAs` (Instagram, Telegram-бот @fclassmsk_bot), `logo` (https://fclass.by/logo.png), `image`. Главный GEO-промах.
**Effort:** 30 мин.

### H5. Перелинковать orphan money-страницы
Добавить ссылки из релевантных блог-постов на `komandirovki-na-vystavki/` (из китайских/выставочных постов) и `concierge/`, усилить ссылки на `komandirovki/`.
**Effort:** 1ч.

---

## 🟡 MEDIUM — в течение месяца

- **M1. Унифицировать NAP** везде: «просп. Победителей, 11, оф. 12» (видимый текст + Schema, desktop+mobile). Установить правильное название БЦ (не Royal Plaza) — уточнить у клиента.
- **M2. Security headers** в `.htaccess`: HSTS (`Strict-Transport-Security`), `X-Frame-Options: SAMEORIGIN`, базовый CSP.
- **M3. width/height всем `<img>`** (CLS). `komandirovki/` hero → WebP + lazy + размеры.
- **M4. Таблицы на `komandirovki/`** (сравнение услуг / чеклист этапов) — для цитируемости AI и rich-content.
- **M5. Дописать тонкие страницы:** concierge (274→600+), visa-guide-2026 (283→600+), turciyu (356→600+).
- **M6. robots.txt:** добавить `Disallow`-правила в каждую AI-bot группу (сейчас они игнорируют запреты из `*`); убрать мёртвые WordPress-disallow и нестандартный `Host:`.
- **M7. sitemap:** проставить реальные `lastmod` по файлам, выровнять priority.
- **M8. dateModified** добавить 3 постам без него.

---

## 🟢 LOW — бэклог

- L1. Удалить избыточный stub `blog/korporativnye-aviabilety-minsk/index.html` (дубль уже обработан canonical+301, но мусор).
- L2. Accessibility (Lighthouse 89→95): контраст, `<main>` landmark, порядок заголовков, aria-hidden focusable, accessible names.
- L3. Best Practices (77): пересмотреть third-party cookies (Metrika/GTM consent).
- L4. Синхронизировать локальную копию llms.txt с live; проверить все URL в llms.txt на 200.
- L5. Добавить /about (entity-страница) для усиления бренд-сигналов.

---

## 📈 Стратегический приоритет (вне технички)

**SQI = 10** — рост упирается в **отсутствие авторитета**, а не технику (SEO 100, ошибок нет). Параллельно с фиксами:
- Наращивать беклинки / упоминания (каталоги РБ, отраслевые порталы, отзывы, PR).
- Развивать брендовые упоминания (соцсети, Telegram, Яндекс.Бизнес отзывы — уже 5.0/47).
- Информационный блог уже работает (поз.1-6 по суточным) — усиливать связку «инфо-пост → money-страница» (H5).

---

## Файлы аудита
- `FULL-AUDIT-REPORT.md` — полный отчёт
- `technical-schema.md` — детали по технике/схеме (субагент)
- `content-onpage.md` — детали по контенту (субагент)
- `geo-images-mobile.md` — детали GEO/картинки/мобайл (субагент)
