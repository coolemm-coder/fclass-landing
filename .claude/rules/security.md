# Security Rules - FirstClass Automation

## Secrets Management

### Текущие секреты (требуют защиты)

| Секрет | Где используется | Статус |
|--------|------------------|--------|
| Telegram Chat ID | n8n workflow | ⚠️ Hardcoded |
| Webhook URLs | HTML/JS файлы | ⚠️ Hardcoded |
| WhatsApp номер | HTML | Публичный (OK) |

### Рекомендации

```javascript
// BAD - hardcoded
fetch('https://emikss.host/webhook/fc-audit', ...)

// BETTER - config object
const CONFIG = {
  webhookUrl: 'https://emikss.host/webhook/fc-audit',
  // В production можно загружать из env
};
fetch(CONFIG.webhookUrl, ...)
```

### .gitignore

```
.env
.env.local
*.log
.vercel
node_modules/
```

---

## Form Security

### Input Validation (Client-side)

```javascript
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
}

function sanitizeInput(input) {
  return input.replace(/<[^>]*>/g, ''); // Remove HTML tags
}
```

### Required Fields

```html
<input type="email" name="email" required>
<input type="tel" name="phone" pattern="[0-9+\-\s]+" required>
```

### Server-side Validation (n8n)

```javascript
// В Code node
const data = $input.first().json;

// Проверка обязательных полей
if (!data.role || !data.name) {
  return [{
    json: {
      error: true,
      message: 'Missing required fields'
    }
  }];
}

// Sanitize
data.name = data.name.substring(0, 100); // Limit length
```

---

## Vercel Security Headers

### vercel.json

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
```

---

## CORS (n8n Webhooks)

### Если CORS ошибки

n8n автоматически добавляет CORS headers. Если проблемы:

```javascript
// В Respond to Webhook node
return {
  headers: {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type'
  },
  body: { success: true }
};
```

---

## Data Privacy

### Что собираем

- Имя и роль сотрудника
- Ответы на вопросы аудита
- Временные метки

### Что НЕ собираем

- Пароли
- Финансовые данные клиентов
- Персональные данные клиентов агентства

### Хранение

- Telegram: сообщения в приватном чате (не публичные)
- n8n: временно в памяти (до рестарта)
- TODO: добавить Google Sheets для постоянного хранения

---

## Incident Response

### При компрометации Chat ID

1. Создать новый приватный чат
2. Обновить Chat ID в n8n workflow
3. Проверить историю — нет ли утечки

### При взломе Vercel

1. Войти в Vercel dashboard
2. Проверить deployments
3. Rollback к предыдущей версии если нужно
4. Сменить пароль Vercel

### При взломе n8n

1. Проверить активные workflows
2. Деактивировать подозрительные
3. Сменить n8n пароль
4. Проверить webhooks — нет ли лишних
