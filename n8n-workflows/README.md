# N8N Workflows для automation.landingpro.by

Три webhook'а для приёма лидов с fclass.by и landingpro.by.

## Импорт

1. Открой https://automation.landingpro.by
2. Каждый файл `*.workflow.json` импортируй: **Workflows → + → Import from File**
3. **ВАЖНО:** в node «Telegram уведомление» подставь credentials `@travelangelby_bot` для fclass и `@landingproby_bot` для LandingPro
4. Для fclass укажи групповой chat_id через env `FCLASS_LEADS_CHAT_ID` или замени `-100REPLACE_WITH_GROUP_ID` в Telegram node
5. Активируй workflow (toggle справа сверху)
6. Скопируй Webhook URL из node «Webhook» (он автоматически будет вида https://automation.landingpro.by/webhook/X)

## После импорта

Webhook'и должны быть **именно с этими paths** (это в коде форм на сайтах):
- `https://automation.landingpro.by/webhook/fclass-blog-lead` — формы в блог-постах fclass
- `https://automation.landingpro.by/webhook/fclass-pdf-lead` — форма захвата PDF на /resources/dogovor-template/
- `https://automation.landingpro.by/webhook/lp-lead` — формы на лендингах landingpro

Если n8n назначит другие paths — измени параметр Path в Webhook node на эти три.

## Логика каждого workflow

1. Webhook принимает POST с полями (company / phone / email / source / page / [task])
2. Set node форматирует красивое сообщение
3. Telegram node отправляет квалифицированную заявку в группу лидов First Class
4. Опционально: HTTP node добавляет в U-ON CRM (отключён по умолчанию, нужно добавить API token)
5. Webhook возвращает 200 OK

## Как получить chat_id группы

1. Добавь `@travelangelby_bot` в нужную Telegram-группу.
2. Напиши любое сообщение в группе.
3. Получи `chat.id` через `getUpdates` у бота или временно добавь `@RawDataBot`.
4. В n8n задай env `FCLASS_LEADS_CHAT_ID=-100...` либо вставь этот ID в Telegram node.

Не возвращать личный `543428212` как основной канал: заявки должны уходить в рабочую группу, чтобы менеджеры не теряли лиды.
