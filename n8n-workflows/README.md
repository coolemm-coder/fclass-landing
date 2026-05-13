# N8N Workflows для emikss.host

Три webhook'а для приёма лидов с fclass.by и landingpro.by.

## Импорт

1. Открой https://emikss.host
2. Каждый файл `*.workflow.json` импортируй: **Workflows → + → Import from File**
3. **ВАЖНО:** в node «Telegram уведомление» подставь credentials своего @landingproby_bot
4. Активируй workflow (toggle справа сверху)
5. Скопируй Webhook URL из node «Webhook» (он автоматически будет вида https://emikss.host/webhook/X)

## После импорта

Webhook'и должны быть **именно с этими paths** (это в коде форм на сайтах):
- `https://emikss.host/webhook/fclass-blog-lead` — формы в блог-постах fclass
- `https://emikss.host/webhook/fclass-pdf-lead` — форма захвата PDF на /resources/dogovor-template/
- `https://emikss.host/webhook/lp-lead` — формы на лендингах landingpro

Если n8n назначит другие paths — измени параметр Path в Webhook node на эти три.

## Логика каждого workflow

1. Webhook принимает POST с полями (company / phone / email / source / page / [task])
2. Set node форматирует красивое сообщение
3. Telegram node отправляет тебе в чат (chat_id из CLAUDE.md = 543428212)
4. Опционально: HTTP node добавляет в U-ON CRM (отключён по умолчанию, нужно добавить API token)
5. Webhook возвращает 200 OK
