# Architecture - FirstClass Automation (Updated 2026-02-07)

## Stack

| Layer | Technology |
|-------|-----------|
| Лендинг | HTML5 + CSS3 + Vanilla JS (all-in-one index.html) |
| Хостинг | Vercel (fclass-landing.vercel.app) |
| Автоматизация | n8n (automation.landingpro.by, Beget) |
| Уведомления | Telegram Bot API |
| CRM | Google Sheets (планируется) |
| Карты | Яндекс.Карты (embed) |
| Аналитика | Яндекс.Метрика (код добавлен, ID pending) |

## System Flow (текущий)

```
Клиент (B2B компания)
        |
   +----+----+
   |    |    |
Лендинг  WhatsApp  Телефон
(fclass.by)
   |
Форма заявки
   |
   v (TODO: подключить)
n8n Webhook (automation.landingpro.by)
   |
   +--------+---------+--------+
   |        |         |        |
Telegram  GSheets   Email   Авто-ответ
(менеджер) (CRM)  (клиент) (клиент)
```

## Endpoints

| Endpoint | Purpose | Status |
|----------|---------|--------|
| fclass-landing.vercel.app | Лендинг B2B | Active |
| fc-audit.vercel.app | Web-panel аудита | Active |
| automation.landingpro.by/webhook/fc-audit | n8n аудит webhook | Active |
| automation.landingpro.by/webhook/fc-lead | n8n leads webhook | TODO |
| automation.landingpro.by/webhook/tour-search-unified | Tour Search API | Active |

## Project Structure

```
FirstClass_Automation/
├── CLAUDE.md              # AI контекст
├── PROJECT_LOG.md         # Журнал + статус
├── VISION.md              # Цели + KPI
├── ROADMAP.md             # План с дедлайнами
│
├── fclass-landing/        # B2B лендинг
│   ├── index.html         # 893 строки, all-in-one
│   ├── hero.jpg           # Фото (секция "О нас")
│   ├── logo.png           # Логотип
│   └── vercel.json
│
├── web-panel/             # Аудит-панель
├── questionnaires/        # Анкеты
├── n8n/workflows/         # Workflow JSON
├── docs/                  # Документация
├── data/                  # Справочники
│
└── .claude/
    ├── business-rules.md
    ├── memory/            # architecture, decisions, gotchas, learnings
    ├── rules/             # coding-style, git-workflow, security
    ├── skills/            # project-context, self-improve
    └── sessions/          # Логи сессий (YYYY-MM-DD.md)
```

## Лендинг: секции

| # | Секция | Фон | Контент |
|---|--------|-----|---------|
| 1 | Nav | rgba(navy, 0.95) | Logo + меню + CTA |
| 2 | Hero | Unsplash фото | "Командировки под ключ" |
| 3 | Services | #e2e6eb | 4 карточки услуг |
| 4 | Philosophy | #e2e6eb | "Как мы работаем" |
| 5 | Expertise | var(--primary) navy | "О нас" + фото + бейдж |
| 6 | Trust | #e2e6eb | 4 цифры (8 лет, 15 мин...) |
| 7 | Contact | #e2e6eb | Форма + контакты |
| 8 | Map | #e2e6eb | Яндекс.Карты |
| 9 | Footer | var(--charcoal) | 4 колонки |

## Связь с FC_LeadRouter

Общий n8n сервер (automation.landingpro.by). Tour Search API и Telegram Bot из FC_LeadRouter могут быть адаптированы для First Class.
