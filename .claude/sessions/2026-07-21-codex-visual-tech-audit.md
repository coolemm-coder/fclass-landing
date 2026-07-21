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

## Что важно не перепутать

В `rg` по всему repo встречаются старые `15 минут`, `emikss.host`, `AggregateRating`, скидки и "туры", но значительная часть находится в `audit-artifacts/`, `docs/`, `questionnaires/`, `web-panel/` и не участвует в публичном деплое. Перед массовой правкой обязательно отделять deployable public files от архивов и внутренних материалов.

`komandirovki/index.html` намеренно содержит блок "Почему это не туры" - это соответствует правке пользователя: акцент на командировки и билеты, не турпакеты.

## Следующий приоритет

Если продолжать аудит, следующий полезный шаг - пройти route-pages из `/tickets/minsk-*` на длину title и единый шаблон CTA/тарифов, но не смешивать это с текущим фикс-пакетом.
