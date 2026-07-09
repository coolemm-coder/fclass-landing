# Skill: Project Context Loader

## Description

Загружает контекст проекта FirstClass_Automation в начале сессии.

## Trigger

Используй этот skill когда:
- Начинаешь работу с проектом
- Нужно вспомнить архитектуру
- Перед изменением лендинга или web-panel

## Instructions

### 1. Загрузи основной контекст

```bash
# Прочитай CLAUDE.md
cat /Users/admin/Desktop/FirstClass_Automation/CLAUDE.md
```

### 2. Проверь известные проблемы

```bash
# ОБЯЗАТЕЛЬНО перед любыми изменениями
cat /Users/admin/Desktop/FirstClass_Automation/.claude/memory/gotchas.md
```

### 3. Проверь текущий статус

```bash
# Статус Vercel deployments
cd /Users/admin/Desktop/FirstClass_Automation/fclass-landing
npx vercel ls 2>/dev/null | head -10

# Проверить что есть в проекте
ls -la /Users/admin/Desktop/FirstClass_Automation/
```

### 4. Для работы с лендингом

```bash
# Структура лендинга
ls -la /Users/admin/Desktop/FirstClass_Automation/fclass-landing/

# Главная страница
head -100 /Users/admin/Desktop/FirstClass_Automation/fclass-landing/index.html
```

### 5. Для работы с web-panel

```bash
# Структура web-panel
ls -la /Users/admin/Desktop/FirstClass_Automation/web-panel/pages/

# Одна из анкет
head -50 /Users/admin/Desktop/FirstClass_Automation/web-panel/pages/dasha.html
```

### 6. Для работы с n8n

```bash
# Workflow файл
cat /Users/admin/Desktop/FirstClass_Automation/n8n/workflows/fc_audit_webhook.json
```

## Quick Reference

| Компонент | Путь |
|-----------|------|
| Лендинг | `fclass-landing/` |
| Web-panel | `web-panel/` |
| Анкеты (MD) | `questionnaires/` |
| n8n workflow | `n8n/workflows/fc_audit_webhook.json` |
| Roadmap | `docs/ROADMAP.md` |

## Production URLs

| URL | Назначение |
|-----|-----------|
| https://fclass-landing.vercel.app | Лендинг |
| https://fc-audit.vercel.app | Web-panel |
| https://automation.landingpro.by/webhook/fc-audit | n8n webhook |

## Output

После загрузки контекста, сообщи:
- Текущая фаза проекта (из CLAUDE.md)
- Статус deployments
- Последние изменения (git log -3)
