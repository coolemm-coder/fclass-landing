# Learnings - FirstClass Automation

## Vercel Deploy

### Команда деплоя

```bash
cd /Users/admin/Desktop/FirstClass_Automation/fclass-landing
npx vercel --prod --yes
```

### vercel.json Конфиг

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Frame-Options", "value": "SAMEORIGIN" }
      ]
    }
  ]
}
```

### Редиректы

```json
{
  "redirects": [
    { "source": "/old-page", "destination": "/new-page", "permanent": true }
  ]
}
```

---

## n8n Webhook Patterns

### Базовый Webhook → Telegram

```
Webhook (POST)
    ↓
Code (Format Message)
    ↓
Telegram (Send Message)
    ↓
Respond to Webhook
```

### Форматирование для Telegram

```javascript
// В Code node
const data = $input.first().json;

let message = `📋 *Новая анкета*\n\n`;
message += `👤 Роль: ${data.role}\n`;
message += `📅 Дата: ${new Date().toLocaleString('ru-RU')}\n\n`;

// Итерация по полям
for (const [key, value] of Object.entries(data)) {
  if (key !== 'role') {
    message += `*${key}:* ${value}\n`;
  }
}

return [{ json: { message } }];
```

### Respond to Webhook

```javascript
// Вернуть JSON клиенту
return [{
  json: {
    success: true,
    message: "Данные получены"
  }
}];
```

---

## Sapphire Dreams Design System

### CSS Variables Setup

```css
:root {
  /* Цвета */
  --primary: #0c1825;
  --primary-light: #1a3a5c;
  --accent: #c9a962;
  --cream: #f8f9fa;
  --white: #ffffff;

  /* Типографика */
  --font-heading: 'Playfair Display', serif;
  --font-body: 'DM Sans', sans-serif;

  /* Spacing */
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 2rem;
  --spacing-lg: 4rem;

  /* Shadows */
  --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.15);
}
```

### Button Styles

```css
.btn-primary {
  background: var(--accent);
  color: var(--primary);
  padding: var(--spacing-sm) var(--spacing-md);
  border: none;
  font-family: var(--font-body);
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}
```

---

## Form Submission (Vanilla JS)

### Базовый паттерн

```javascript
document.getElementById('form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const formData = new FormData(e.target);
  const data = Object.fromEntries(formData.entries());

  try {
    const response = await fetch('https://automation.landingpro.by/webhook/fc-audit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (response.ok) {
      window.location.href = '/thank-you.html';
    } else {
      alert('Ошибка отправки');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Ошибка сети');
  }
});
```

### Валидация перед отправкой

```javascript
function validateForm(data) {
  const required = ['name', 'email', 'role'];
  const missing = required.filter(field => !data[field]);

  if (missing.length > 0) {
    alert(`Заполните обязательные поля: ${missing.join(', ')}`);
    return false;
  }
  return true;
}
```

---

## Responsive Design

### Mobile-First Approach

```css
/* Base (mobile) */
.container {
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 4rem;
  }
}
```

### Touch Targets

```css
/* Минимум 44px для touch */
button, a, input[type="submit"] {
  min-height: 44px;
  min-width: 44px;
}
```

---

## Яндекс.Карты Integration

### Базовая вставка

```html
<script src="https://api-maps.yandex.ru/2.1/?apikey=YOUR_KEY&lang=ru_RU"></script>

<div id="map" style="width: 100%; height: 400px;"></div>

<script>
ymaps.ready(function() {
  const map = new ymaps.Map("map", {
    center: [53.9006, 27.5590], // Минск
    zoom: 15
  });

  // Добавить маркер
  const placemark = new ymaps.Placemark([53.9006, 27.5590], {
    balloonContent: 'First Class Travel'
  });
  map.geoObjects.add(placemark);
});
</script>
```
