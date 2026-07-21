# Claude handoff - visual and technical audit

Дата: 2026-07-21
От Codex для Claude.

## Контекст

Пользователь попросил провести визуальный и технический аудит сайта fclass.by и доделать, что нужно.

## Что проверено на live

Скриншоты и JSON-аудит сохранены локально в `/tmp/fclass-audit-2026-07-21/`.

Страницы:

- `/`
- `/tickets/`
- `/komandirovki/`
- `/tickets/aviabilety-dlya-yurlic/`
- `/tarify/`
- `/resources/calculator/`
- `/cases/`
- `/blog/`

Проверки:

- HTTP status;
- наличие одного H1;
- title/meta description/canonical;
- JSON-LD parsing;
- console errors;
- 4xx/5xx ресурсов fclass.by;
- mobile horizontal overflow;
- missing image alt;
- базовая визуальная проверка desktop/mobile screenshots.

## Вывод аудита

Хорошо:

- все проверенные live-страницы отдают HTTP 200;
- JSON-LD на проверенных live-страницах валиден;
- по live-аудиту нет 4xx/5xx ресурсов fclass.by;
- console errors не найдены;
- missing alt на проверенных money-pages не найден;
- `/tarify/` корректно отображается на desktop/mobile.

Проблемы, которые Codex исправил:

- На mobile у `/komandirovki/` и `/tickets/aviabilety-dlya-yurlic/` был горизонтальный overflow 327px. Причина: inline `grid-template-columns:repeat(3,1fr)` на блоке "Калькулятор и материалы для бухгалтера", который перебивал mobile media query. Inline-стиль удалён, теперь `.grid` переходит в одну колонку.
- У главной страницы meta description был 185 символов. Укорочен до нормального сниппет-диапазона.
- В публичных материалах были остатки старого позиционирования: "корпоративные тарифы", "корпоративные группы/перелёты" и обещания по НДС/ЭСЧФ без оговорки. Исправлено в `/concierge/`, `/blog/aviabilety-dlya-yur-lic.html` и `/blog/korporativnye-aviabilety-minsk.html`.
- В старой статье `/blog/aviabilety-dlya-yur-lic.html` были устаревшие сборы "25-60 BYN" и пример "20 BYN на любой билет". Заменено на текущую тарифную сетку: авиабилет 30 BYN, ж/д билет 20 BYN, проживание 30 BYN, изменение/отмена по правилам поставщика + сервисный сбор.
- В футере `/concierge/` ссылка "Туры и проживание" вела на `/tours/`. `/tours/` уже noindex-redirect на билеты, но как услуга это конфликтовало с текущим позиционированием. Заменено на "Проживание" со ссылкой на `/tarify/`.
- SEO-доводка: сокращён title `/tickets/aviabilety-dlya-yurlic/` до 53 символов и meta description `/concierge/` до нормального диапазона.
- `.htaccess` намеренно 301-редиректит старые blog-страницы `/blog/aviabilety-dlya-yur-lic.html` и `/blog/korporativnye-aviabilety-minsk.html` на money-page `/tickets/aviabilety-dlya-yurlic/`. После проверки live исправлены внутренние ссылки, которые раньше вели на эти редиректы, и обновлён `llms.txt`.
- В `/blog/` была дублирующая карточка на ту же money-page. Одна карточка оставлена для "авиабилеты для юрлиц", вторая заменена на `/tarify/`.
- В FAQ калькулятора убрано слово "скидка" даже в отрицательной формулировке, чтобы оно не попадало в сниппеты и не конфликтовало с позиционированием.

## Что важно не перепутать

В `rg` по всему repo встречаются старые `15 минут`, `emikss.host`, `AggregateRating`, скидки и "туры", но значительная часть находится в `audit-artifacts/`, `docs/`, `questionnaires/`, `web-panel/` и не участвует в публичном деплое. Перед массовой правкой обязательно отделять deployable public files от архивов и внутренних материалов.

`komandirovki/index.html` намеренно содержит блок "Почему это не туры" - это соответствует правке пользователя: акцент на командировки и билеты, не турпакеты.

## Следующий приоритет

Если продолжать аудит, следующий полезный шаг - пройти route-pages из `/tickets/minsk-*` на длину title и единый шаблон CTA/тарифов, но не смешивать это с текущим фикс-пакетом.

## Дополнение Codex - визуальная разгрузка mobile

После повторного визуального аудита Codex внес аккуратный mobile-first cleanup:

- На главной странице в mobile уменьшена высота первого экрана и скрыты плавающие WhatsApp/Telegram-кнопки, чтобы они не перекрывали trust strip. Desktop-правила не менялись.
- На `/komandirovki/` в mobile убран дублирующий `tg-bubble`, оставлена нижняя sticky CTA. Hero и секции стали компактнее только через `@media(max-width:768px)`: в первом экране оставлены первые две метрики и основной CTA, вторичный Telegram в hero скрыт.
- На `/tickets/aviabilety-dlya-yurlic/` в mobile убран дублирующий `tg-bubble`, hero стал ниже, CTA растянут на ширину экрана, а hero-чипы сокращены до первых двух. Вторичный Telegram в hero скрыт, потому что он уже есть в sticky CTA. Desktop не затронут.
- На `/resources/calculator/` в mobile уменьшены hero и отрицательный отступ калькулятора, скрыт `tg-bubble`, оставлена sticky CTA. Также в навигацию добавлена ссылка `/tarify/`.
- На `/tarify/` в mobile скрыт плавающий Telegram-баббл и немного ужат hero. Desktop не затронут.
- На `/blog/` добавлена ссылка `Тарифы` в навигацию и компактные фильтры-разделы после hero. Также исправлен старый неоформленный Telegram-блок внизу страницы: на desktop он стал нормальным fixed bubble, на mobile скрыт. Это единственная осознанная desktop-правка в визуальном cleanup, потому что блог визуально был самым монотонным и навигационно неполным.

Важно: основная часть изменений сделана в mobile media queries, чтобы не менять desktop-верстку money-pages.

## Дополнение Codex - профессиональный quality gate

Codex добавил повторяемый Playwright-аудит сайта:

- `npm run site:audit` - локальный аудит ключевых страниц;
- `npm run site:audit:live` - тот же набор на `https://fclass.by`;
- `npm run site:audit:sitemap` - расширенный проход по sitemap;
- отчеты пишутся в `/tmp/fclass-site-quality-*`.

Последний локальный прогон: `/tmp/fclass-site-quality-2026-07-21T15-12-46-105Z/report.md`.
Последний live-прогон: `/tmp/fclass-site-quality-2026-07-21T15-11-32-749Z/report.md`.
Результат обоих прогонов: `Errors: 0`, `Warnings: 0`.

Что исправлено этим пакетом:

- Добавлена полноценная service landing page `/visa-support/` вместо 301-редиректа на старую blog-страницу. Внутренние ссылки и schema теперь ведут на реальную услугу.
- В `.htaccess` удален redirect `/visa-support/ -> /blog/vizovaya-podderzhka-minsk.html`.
- В `sitemap.xml` добавлен `/visa-support/`.
- На `/tickets/minsk-stambul/` убрана битая ссылка на `/tickets/_route-styles.css`, из-за которой аудит ловил failed resource.
- На route-pages Минск-Москва, Минск-Стамбул, Минск-Баку, Минск-Калининград сокращены title, чтобы не резались в выдаче.
- В `index.html`, `/komandirovki/`, `/tickets/aviabilety-dlya-yurlic/` добавлен `rel="noopener"` для внешних ссылок с `target="_blank"`.
- На `/cases/` в mobile скрыт floating Telegram bubble, когда показан sticky CTA, чтобы не было двух конкурирующих кнопок.
- На `/visa-support/` mobile sticky CTA теперь появляется после скролла, а не перекрывает первый экран.
- На главной и `/komandirovki-na-vystavki/` FAQ-переключатели заменены на семантические `button` с `aria-expanded`.
- На `/komandirovki-na-vystavki/` увеличены anchor-nav touch targets до 44px.

Quality gate проверяет: HTTP status, title/meta/canonical, один H1, JSON-LD parse, missing alt, `target="_blank"` без `rel`, onclick на несемантических элементах, запрещенные обещания/скидки, 4xx/5xx ресурсов, console errors, mobile/tablet/desktop overflow, конкурирующие mobile CTA и маленькие above-fold touch targets.
Для визуальных ассетов (`image`, `media`, `font`) аудит не считает `net::ERR_ABORTED` ошибкой, если файл отдается сервером: Playwright может сам прервать повторную загрузку картинки/видео при смене viewport. 4xx/5xx по этим ресурсам остаются ошибками через response-status check.

Не откатывать без причины:

- новую страницу `/visa-support/`;
- `scripts/site-quality-audit.js`;
- npm scripts `site:audit`, `site:audit:live`, `site:audit:sitemap`;
- удаление redirect для `/visa-support/`.
