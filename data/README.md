# Data Directory — FirstClass_Automation

## Contact Databases

| File | Records | Source | Description |
|------|---------|--------|-------------|
| `all_contacts.csv` | ~3825 | Объединённая | Мастер-база: все контакты из всех источников |
| `whale_targets.csv` | 46 | Ручной отбор | VIP-компании (EPAM, Евроопт, 21vek, банки) |
| `cci_exporters.csv` | ~2794 | cci.by | Экспортёры РБ (Торгово-промышленная палата) |
| `park_by_residents.csv` | ~1048 | park.by | IT-компании, резиденты ПВТ |

### Схема all_contacts.csv

| Column | Type | Description |
|--------|------|-------------|
| name | string | Название компании |
| email | string | Контактный email |
| website | string | URL сайта |
| city | string | Город |
| employees | string | Количество сотрудников |
| category | string | Категория (exporter/it/whale) |
| priority | string | high/medium/low |
| source | string | cci/park/manual |
| phone | string | Телефон |
| description | string | Описание деятельности |

### Схема whale_targets.csv

| Column | Type | Description |
|--------|------|-------------|
| name | string | Название компании |
| category | string | it/bank/retail/manufacturing |
| employees | string | Количество сотрудников |
| email | string | Контактный email |
| website | string | URL сайта |
| phone | string | Телефон |
| city | string | Город |
| priority | int | 1-3 (1 = highest) |
| notes | string | Заметки |

## Email Templates

| File | Status | Description |
|------|--------|-------------|
| `email_templates.md` | ❌ DEPRECATED | v1 — HTML шаблоны (проблемы с доставляемостью) |
| `email_templates_v2_plaintext.md` | ✅ ACTIVE | v2 — Plain text для холодного outreach |

## JSON Data

| File | Source | Description |
|------|--------|-------------|
| `cci_exporters.json` | cci.by | Raw data (парсинг экспортёров) |
| `park_by_residents.json` | park.by | Raw data (парсинг IT-компаний) |

## Subfolders

| Folder | Description |
|--------|-------------|
| `brand/` | Брендинг First Class (логотипы, цвета) |
| `screencasts/` | Записи экрана (аудит, демо) |

---

*Обновлено: 2026-03-27*
