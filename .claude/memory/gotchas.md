# Gotchas - FirstClass Automation

## P1: Важные

### Hardcoded Telegram Chat ID

**Проблема:** Chat ID захардкожен в n8n workflow

**Где:** `n8n/workflows/fc_audit_webhook.json`
```json
"chatId": "543428212"
```

**Риск:** При смене чата нужно редактировать workflow

**Решение:**
1. Использовать n8n credentials
2. Или environment variable: `$env.TELEGRAM_CHAT_ID`

**Статус:** ⚠️ Работает, но требует улучшения

---

### Webhook URLs в HTML

**Проблема:** URLs хардкодированы в JavaScript

**Где:** `web-panel/js/*.js`
```javascript
fetch('https://emikss.host/webhook/fc-audit', ...)
```

**Риск:** При смене сервера нужно менять во всех файлах

**Решение:**
```javascript
const CONFIG = {
  webhookUrl: 'https://emikss.host/webhook/fc-audit'
};
// Использовать: CONFIG.webhookUrl
```

**Статус:** ⚠️ Работает, но требует рефакторинга

---

### Нет .env файлов

**Проблема:** Конфигурация разбросана по файлам

**Симптом:** Сложно найти все настройки

**Решение:** Создать `.env.example`:
```env
VERCEL_URL=https://fclass-landing.vercel.app
N8N_HOST=https://emikss.host
TELEGRAM_CHAT_ID=543428212
WHATSAPP_NUMBER=375447725266
```

**Статус:** 📋 TODO

---

## P2: Средние

### Нет Аналитики

**Проблема:** Google Analytics / Яндекс.Метрика не подключены

**Симптом:** Не знаем сколько посетителей на лендинге

**Решение:**
1. Добавить Google Analytics 4
2. Или Яндекс.Метрика (для РБ аудитории)

**Где добавить:** `fclass-landing/index.html` в `<head>`

**Статус:** 📋 TODO

---

### Карта Без Точного Адреса

**Проблема:** Яндекс.Карта на лендинге без маркера офиса

**Где:** `fclass-landing/index.html`

**Симптом:** Посетители не видят точное расположение

**Решение:** Получить адрес офиса и добавить placemark

**Статус:** 📋 Ждём данные от клиента

---

### Данные Только в Памяти n8n

**Проблема:** Ответы анкет хранятся in-memory

**Симптом:** При рестарте n8n данные теряются

**Риск:** Потеря заполненных анкет

**Решение:**
1. Добавить Google Sheets интеграцию
2. Или Firebase/Notion

**Статус:** 📋 TODO после основного аудита

---

## Vercel Специфичные

### Vercel Не Поддерживает PHP

**Проблема:** Vercel только для статики и serverless

**Симптом:** Нельзя использовать PHP для форм

**Решение:**
- Формы отправляем на n8n webhook
- Или Vercel Serverless Functions (Node.js)

**Учитывать при:** Добавлении backend логики

---

### CORS на Webhook

**Проблема:** Браузер может блокировать cross-origin запросы

**Симптом:** Форма не отправляется, ошибка в консоли

**Решение:** n8n webhook автоматически добавляет CORS headers

**Если проблема:**
```javascript
// В n8n Respond node добавить headers
{
  "Access-Control-Allow-Origin": "*"
}
```

---

## HTML/CSS Специфичные

### CSS Variables Не Работают в IE

**Проблема:** CSS Custom Properties (--primary и т.д.)

**Симптом:** Стили не применяются в IE11

**Решение:** IE11 не поддерживается (2% трафика)

**Если нужна поддержка:** Использовать PostCSS autoprefixer

---

### Шрифты Не Загружаются

**Проблема:** Google Fonts могут быть медленными

**Симптом:** FOUT (Flash of Unstyled Text)

**Решение:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preload" href="font.woff2" as="font" crossorigin>
```

**Статус:** ✅ Уже настроено в лендинге
