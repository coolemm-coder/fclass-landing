# Claude handoff — fclass.by leads / SEO / GEO audit

Дата: 2026-07-14
От Codex для Claude.

## Контекст

Пользователь просит понять, почему нет лидов, как продвигаться и как выйти в топ. Я провел live-аудит и сохранил артефакты.

Главный отчет: `AUDIT_2026-07-14_LEADS_SEO_GEO_AI_TOP.md`
Live HTML snapshots: `audit-artifacts/2026-07-14/`

## Важное перед правками

Локальная ветка `main` отстает от `origin/main` на 92 коммита. Не править и не деплоить старый локальный checkout без синхронизации, иначе можно откатить критические фиксы.

`git status` на момент аудита:

```text
## main...origin/main [behind 92]
?? .claude/sessions/2026-06-13-codex-full-audit.md
?? AUDIT_2026-06-13_SEO_GEO_AI_VISUAL.md
?? CLAUDE_AUDIT_HANDOFF_2026-06-14.md
?? CLAUDE_VISUAL_REWORK_BRIEF.md
?? audit-artifacts/
```

Есть риск untracked conflict при `git pull`: локальный `CLAUDE_VISUAL_REWORK_BRIEF.md` уже может пересекаться с файлом из `origin/main`.

## Самая вероятная причина отсутствия лидов

В `origin/main` найден критический коммит:

```text
54acc1b fix(critical): migrate all webhooks emikss.host -> automation.landingpro.by (old domain expired 2026-07-06, lead forms were silently failing)
```

Также:

```text
55cf8ac chore(deploy): force re-sync tickets/index.html (was serving empty body on live site)
94e3089 chore(deploy): force re-sync komandirovochnye-kalkulyator/index.html (was serving empty body on live site)
```

Вывод: часть заявок могла не доходить, а коммерческие страницы могли быть пустыми/битым live-контентом.

## Что я проверил на live

Скачаны:

- `home.html`
- `tickets.html`
- `komandirovki.html`
- `yurlic.html`
- `calc.html`
- `cases.html`
- `blog.html`
- `dogovor.html`
- `robots.txt`
- `sitemap.xml`
- `llms.txt`

Наблюдения:

- live sitemap содержит 55 URL;
- robots содержит sitemap и разрешения для AI-ботов;
- llms.txt есть, но еще содержит "15 минут";
- live УНП в проверенных страницах: `193218120`;
- главная имеет H1, который текстово извлекается как `Авиабилетыдля организаций и физлиц`;
- главная содержит `AggregateRating 5.0 / 44`;
- на нескольких страницах еще встречается "15 минут";
- `/tickets/` имеет форму на `automation.landingpro.by/webhook/fc-lead`, но события аналитики по HTML выглядят слабее, чем на других страницах;
- GET/HEAD на `automation.landingpro.by/webhook/fc-lead` возвращает 404, это может быть нормально для n8n webhook, который принимает только POST;
- `/api/lead-magnet.php` отвечает 405 на GET, значит endpoint жив и запрещает неправильный метод.

## Следующие правки по приоритету

1. Сначала синхронизировать локальную ветку с `origin/main`, сохранив audit/handoff файлы.
2. Сделать end-to-end тест формы только с разрешения пользователя, потому что тест может уйти в Telegram-группу.
3. Убрать или смягчить:
   - `15 минут`;
   - скидки `15-25%`;
   - неподтвержденный `AggregateRating`;
   - любые жесткие обещания по НДС/ЭСЧФ.
4. Исправить H1/разметку главной, чтобы не было `Авиабилетыдля`.
5. Проверить ссылку на Яндекс-карточку First Class и блок отзывов: пользователь просил Яндекс, а не Google.
6. Добавить/проверить цели аналитики на `/tickets/`.
7. Усилить money-page `/tickets/aviabilety-dlya-yurlic/` под:
   - авиабилеты для юр лиц;
   - по безналичному расчету;
   - счет/акт/договор;
   - НДС/ЭСЧФ с аккуратной формулировкой;
   - ИП/ООО;
   - билеты в командировку.
8. После правок отправить URL на переобход: Яндекс.Вебмастер, Google Search Console, IndexNow.

## Codex changes after user approval

Выполнено после аудита:

- Локальная ветка fast-forward синхронизирована с `origin/main` до `f21e573`.
- Локальный untracked `CLAUDE_VISUAL_REWORK_BRIEF.md`, который конфликтовал с tracked-файлом из `origin/main`, сохранён в `/Users/admin/Documents/Codex/fclass-local-backup-2026-07-14/CLAUDE_VISUAL_REWORK_BRIEF.local-before-sync.md`.
- Убран неподтверждённый `AggregateRating 5.0/44` из schema.org на главной.
- Смягчены публичные обещания `15 минут` на главной, `/komandirovki/`, `/komandirovochnye-kalkulyator/`, `llms.txt`, `/komandirovki-na-vystavki/`, части blog CTA и `mobile-preview.html`.
- Исправлен критичный старый webhook в `/blog/komandirovka-v-oae-2026.html`: `emikss.host` -> `automation.landingpro.by`.
- На `/tickets/` добавлен GA4, цель Метрики `LEAD` при успешной отправке формы и события для Telegram/WhatsApp/phone/email кликов.
- В старом content-файле `content/blog/fclass-blog-2026-04-01.html` убраны обещания `15–25%` и `предложение за 15 минут` даже несмотря на то, что `content/` исключён из деплоя.
- Отправлена тестовая заявка `CODEX TEST` на `https://automation.landingpro.by/webhook/fc-lead`; endpoint вернул `HTTP 200` и `{"success":true,"message":"Заявка принята"}`.

Перед деплоем проверь:

- `git diff --check`
- поиск по публичным файлам на `emikss.host`, `AggregateRating`, `15 минут`, `15-25%`/`15–25%` именно в deployable путях;
- доставку тестовой заявки `CODEX TEST` в Telegram-группу/таблицу/CRM, потому что HTTP 200 подтверждает приём endpoint, но не гарантирует, что менеджерское уведомление дошло.

## Конкурент TOPAVIA

Проверял `https://topavia.by/for_business/`.

Они сильны в прямом позиционировании:

- title/H1 про авиабилеты для юрлиц и бизнес;
- 24/7;
- персональный менеджер;
- документы;
- ЭДО;
- отсрочка платежа/депозит;
- реквизиты/УНП на странице.

First Class может обойти честностью, бухгалтерской точностью, понятным процессом по безналу, сильной локальной карточкой Яндекса и кейсами.
