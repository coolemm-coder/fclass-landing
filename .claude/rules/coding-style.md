# Coding Style Rules (HTML/CSS/JS)

## HTML

### Document Structure

```html
<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="...">
  <title>Page Title | First Class</title>

  <!-- Preconnect for fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">

  <!-- Styles -->
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <!-- Header -->
  <header>...</header>

  <!-- Main content -->
  <main>...</main>

  <!-- Footer -->
  <footer>...</footer>

  <!-- Scripts at end -->
  <script src="/js/main.js"></script>
</body>
</html>
```

### Semantic HTML

```html
<!-- GOOD -->
<nav>...</nav>
<main>...</main>
<article>...</article>
<section>...</section>
<aside>...</aside>

<!-- BAD -->
<div class="nav">...</div>
<div class="main">...</div>
```

### Accessibility

```html
<!-- Images -->
<img src="tour.jpg" alt="Описание изображения">

<!-- Forms -->
<label for="email">Email</label>
<input type="email" id="email" name="email" required>

<!-- Buttons -->
<button type="submit" aria-label="Отправить форму">Отправить</button>
```

---

## CSS

### File Organization

```css
/* 1. Variables */
:root {
  --primary: #0c1825;
  --accent: #c9a962;
}

/* 2. Reset/Normalize */
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

/* 3. Base elements */
body { ... }
h1, h2, h3 { ... }
a { ... }

/* 4. Layout */
.container { ... }
.grid { ... }

/* 5. Components */
.btn { ... }
.card { ... }

/* 6. Utilities */
.text-center { ... }
.mt-1 { ... }

/* 7. Media queries (at end) */
@media (min-width: 768px) { ... }
```

### Naming Convention (BEM-like)

```css
/* Block */
.card { ... }

/* Element */
.card__title { ... }
.card__image { ... }

/* Modifier */
.card--featured { ... }
.btn--primary { ... }
```

### CSS Variables

```css
/* GOOD - use variables */
.btn {
  background: var(--accent);
  color: var(--primary);
}

/* BAD - hardcoded */
.btn {
  background: #c9a962;
  color: #0c1825;
}
```

---

## JavaScript

### ES5+ (для совместимости)

```javascript
// GOOD - ES5+
var form = document.getElementById('form');
form.addEventListener('submit', function(e) {
  e.preventDefault();
  // ...
});

// AVOID - ES6+ без transpiler
// const, let, arrow functions работают в современных браузерах
// но для максимальной совместимости используй var + function
```

### DOM Manipulation

```javascript
// GOOD - getElementById (быстрее)
var element = document.getElementById('my-id');

// GOOD - querySelector (гибче)
var element = document.querySelector('.my-class');

// AVOID - jQuery (не нужен для простых задач)
// $('#my-id')
```

### Event Handling

```javascript
// GOOD - addEventListener
button.addEventListener('click', handleClick);

// AVOID - inline handlers
// <button onclick="handleClick()">
```

### Fetch API

```javascript
// GOOD - async/await
async function submitForm(data) {
  try {
    var response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error('Network error');
    }

    return await response.json();
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
```

---

## File Naming

```
pages/
├── index.html          # lowercase
├── thank-you.html      # kebab-case
├── dasha.html          # lowercase

css/
├── style.css           # main styles
├── components.css      # components

js/
├── main.js             # main script
├── form-handler.js     # kebab-case
```

---

## Quality Checklist

Before commit:

- [ ] HTML validates (no errors in W3C validator)
- [ ] Semantic HTML tags used
- [ ] Alt text on all images
- [ ] Labels for all form inputs
- [ ] CSS variables for colors
- [ ] Mobile-first responsive
- [ ] No inline styles (except for dynamic values)
- [ ] No console.log in production
- [ ] Forms have validation
- [ ] Error handling for fetch
