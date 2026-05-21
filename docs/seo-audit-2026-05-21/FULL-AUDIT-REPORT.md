# Полный SEO-аудит fclass.by — 2026-05-21

**Сайт:** https://fclass.by · **Бизнес:** First Class — организация командировок, авиабилеты для физлиц и юрлиц (Минск, Беларусь) · **Тип:** B2B+B2C travel / business-trips agency · ООО «Первый класс», УНП 193582943, с 2018.

---

## Executive Summary

### 🎯 SEO Health Score: **74 / 100** — «Хорошо, но есть чёткие точки роста»

| Категория | Вес | Оценка | Вклад |
|---|---|---|---|
| Technical SEO | 22% | 72 | 15.8 |
| Content Quality | 23% | 70 | 16.1 |
| On-Page SEO | 20% | 75 | 15.0 |
| Schema / Structured Data | 10% | 70 | 7.0 |
| Performance (CWV) | 10% | 85 | 8.5 |
| AI Search Readiness | 10% | 78 | 7.8 |
| Images | 5% | 70 | 3.5 |
| **ИТОГО** | | | **≈74** |

**Lighthouse (desktop+mobile одинаково):** SEO **100** · Accessibility **89** · Best Practices **77** · CLS **0**.
**Yandex Webmaster:** SQI **10** (низкий авторитет), в поиске **49** страниц, исключено 30. Фатальных/критических проблем — нет. 🔴 **NOT_MOBILE_FRIENDLY — PRESENT** (обновлено 20.05.2026).

### 🔴 Топ-5 критичных проблем
1. **Mobile-first провал.** Сайт отдаёт мобильным UA отдельный `mobile-preview.html` — он несёт ~40% контента десктопа и **1 из 4 schema-блоков** (только TravelAgency; нет FAQPage/Service/BreadcrumbList). Google/Яндекс индексируют именно мобильную версию → теряются rich-results, FAQ, хлебные крошки, бОльшая часть текста и ссылок. Яндекс уже пометил `NOT_MOBILE_FRIENDLY`.
2. **Каннибализация Стамбул.** `tickets/minsk-istanbul/` и `tickets/minsk-stambul/` — одинаковый H1 «Авиабилеты Минск — Стамбул 2026», каждая self-canonical. Две страницы конкурируют за один транзакционный запрос.
3. **Каннибализация «суточные».** 3 поста перекрываются: `sutochnye-komandirovka-2026` (1305 слов, pillar), `sutochnye-s-4-aprelya-2026` (818), `sutochnye-komandirovki-aprel-2026` (494, тонкий).
4. **2 запрещённые фразы в проде:** «корпоративного договора» в `organizaciya-komandirovok.html`, «полный комплект документов» в `korporativnye-aviabilety-minsk.html` (нарушают правила проекта).
5. **E-E-A-T слабый на YMYL-кластере.** У всех 30 блог-постов `author` = Organization, нет живого автора; только 4/30 с видимой подписью — плохо для финансово-визовых тем (суточные, визы).

### 🟢 Топ-5 быстрых побед
1. Добавить `sameAs` (Instagram, Telegram), `logo`, `image` в Organization/TravelAgency schema — главный GEO-промах.
2. 301 `minsk-stambul` → `minsk-istanbul` (или canonical) — снять каннибализацию.
3. Унифицировать NAP: везде «просп. Победителей, 11, оф. 12» (сейчас десктоп «11», мобайл «11, оф.12»).
4. Добавить `width`/`height` всем `<img>` (сейчас нет нигде — риск CLS), `komandirovki/` hero перевести на WebP+lazy.
5. Убрать 2 запрещённые фразы; добавить таблицы на `komandirovki/` (0 таблиц — слабая цитируемость для AI).

---

## 1. Technical SEO — 72/100

**✅ Хорошо:**
- robots.txt корректен, AI-краулеры (GPTBot, ClaudeBot, PerplexityBot, Google-Extended) явно разрешены.
- sitemap.xml (53 URL) валиден, покрытие хорошее — нет реально потерянных важных страниц и orphans.
- Канониклы чистые, **нет ссылок на vercel.app / чужой домен** (дубль vercel.app закрыт 308-редиректом 21.05).
- Редиректы — чистые одношаговые 301 (`minsk-istanbul→stambul`, blog trailing-slash→`.html`, `/mobile-preview.html→/`, `/tours/→/tickets/`).
- Yandex: нет DNS/5xx/SSL/soft-404/дублей.

**🔴 High:**
- **Mobile-first parity gap** (см. Executive Summary #1). Единственный самый большой риск.

**🟡 Medium:**
- **UA-sniffing на одном URL** — разный HTML по User-Agent, нет `Vary: User-Agent`. Cloaking-adjacent (намерение честное — title/canonical/robots совпадают, риск санкций низкий, но mobile-first штрафует именно за расхождение глубины).
- **Security headers отсутствуют** (live curl): нет HSTS, X-Frame-Options, CSP. Есть только `X-Content-Type-Options: nosniff` и `Referrer-Policy`.
- **NAP-несогласованность в schema:** mobile «пр. Победителей, 11, оф. 12» vs index «просп. Победителей, 11».

**🟢 Low:**
- robots.txt: per-bot группы (GPTBot и т.д.) не наследуют `Disallow` из `*` — именованные боты игнорируют запреты. Нестандартная строка `Host:`, мёртвые WordPress-disallow.
- sitemap: `lastmod` массово проштампован `2026-05-15`, priority завышены.

---

## 2. Content Quality — 70/100

**✅ Хорошо:**
- Блог-кластер ранжируется по «командировочные/суточные 2026» на **позициях 1-6** (топ-клики Вебмастера). Бренд «первый класс турагентство» — поз.2.
- Все 29 постов с `datePublished`, 25 с `dateModified`. УНП на 37 страницах.
- Tickets-кластер хорошо подпитан внутренними ссылками (29 постов ссылаются).

**🔴 Critical/High:**
- **Каннибализация Стамбул** (Critical) и **суточные ×3** (High) — см. Executive Summary.
- **E-E-A-T слабый** (High): нет именных авторов на YMYL-темах.
- **2 запрещённые фразы live** (High).

**🟡 Medium:**
- **Orphan money-страницы:** 0 постов ссылаются на `komandirovki-na-vystavki/` и `concierge/`; только 2 — на `komandirovki/`.
- **Тонкий контент:** concierge (274 сл.), visa-guide-2026 (283), turciyu (356), ряд ticket-страниц <450 слов.
- **Mobile parity:** мобайл 465 слов vs десктоп 819 (-43%), 6 H2 vs 8.

**Cleared (не нарушения):** фиксированных обещаний скидок нет; «корпоративные авиабилеты» как оффер не используется (везде «договор для юрлиц»); туристические формулировки на бизнес-страницах контекстно ок.

---

## 3. On-Page SEO — 75/100

**✅:** Все публичные страницы имеют title, meta description, ровно один H1, canonical. Иерархия заголовков без пропусков уровней.

**🔴/🟡:**
- Дублирующийся title istanbul/stambul; istanbul title 96 символов (обрезается в выдаче).
- Orphan money-страницы (см. выше).
- 3 поста без `dateModified`.

---

## 4. Schema / Structured Data — 70/100

**✅:** TravelAgency, FAQPage, BreadcrumbList, Service, Article — весь JSON-LD парсится валидно.

**🔴/🟡:**
- **Mobile: только 1/4 schema** (TravelAgency); нет FAQPage/Service/BreadcrumbList — теряются rich-results под mobile-first.
- **Нет `sameAs`** (IG/Telegram есть в HTML, но не в графе сущности) — главный GEO-промах.
- Нет `logo`/`image` в schema, нет /about.
- NAP-несогласованность (см. Technical).

---

## 5. Performance (CWV) — 85/100

**✅:** Статический HTML, **CLS = 0**, Lighthouse SEO 100. Hero через `<picture>`+WebP. Быстрый отклик (Yandex SLOW_AVG_RESPONSE_TIME — ABSENT).

**🟡:**
- **Ни у одного `<img>` нет width/height** — риск CLS на внутренних страницах.
- `komandirovki/` hero — сырой JPG без WebP/lazy/размеров (худшая страница).
- Best Practices 77: third-party cookies (Metrika/GTM), записи в Issues-панели.
- Поле CrUX недоступно (GSC/CrUX не подключены) — оценка по лабораторным данным.

---

## 6. AI Search Readiness (GEO) — 78/100

**✅:**
- **llms.txt — сильный (A-)**: spec-compliant, есть quotable факт-блок и раздел «авиа-санкции 2026» (то, что AI охотно цитирует).
- AI-краулеры разрешены.
- Хорошая цитируемость: блог-кластер + `komandirovki-na-vystavki/` (7 таблиц) с FAQPage и датированными фактами.

**🟡:**
- Per-bot Disallow trap (см. Technical Low).
- Нет `sameAs`/entity-сигналов.
- `komandirovki/` (главная money-страница) — **0 таблиц**, слабая цитируемость.
- Локальная копия llms.txt рассинхронизирована с live.

---

## 7. Images — 70/100

**✅:** У всех контентных картинок есть alt; hero — `<picture>`+WebP.
**🟡:** Нет width/height нигде (CLS); `komandirovki/` hero — сырой JPG.

---

## 8. Accessibility (Lighthouse 89)

Провалы: контраст текст/фон, `[aria-hidden=true]` с фокусируемыми потомками, непоследовательный порядок заголовков, отсутствие `<main>` landmark, несовпадение видимых лейблов и accessible names. Это влияет и на UX, и косвенно на качество для краулеров.

---

## Контекст: трафик и авторитет

- **SQI = 10** — почти нет авторитета. Главный стратегический барьер (нет беклинков/упоминаний), а не техника.
- Трафик идёт с **информационных** запросов (суточные/командировочные) на блог; **денежные** страницы (tickets/командировки) органики почти не получают.
- 1133 запроса за неделю, но клики единичные (1-4) — низкий общий объём.

**Вывод:** техническая база здоровая (SEO 100, нет фатальных ошибок), но рост упирается в (1) mobile-first провал, (2) каннибализацию/E-E-A-T контента и (3) отсутствие авторитета (SQI 10). Приоритет — исправить мобильную версию и контентные дубли, параллельно строить ссылочную массу/упоминания.

См. `ACTION-PLAN.md` для приоритизированного плана.
