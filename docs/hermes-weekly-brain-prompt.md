# Hermes Weekly Brain — SEO дайджест с действиями

Запускается каждое воскресенье 19:00 MSK через cron на Beget VPS (Hermes Gateway).
Заменяет молчаливый "fclass + landingpro" мониторинг на дайджест с конкретными действиями.

## Cron на VPS

```cron
0 19 * * 0 /root/.hermes/scripts/weekly-brain.sh >> /var/log/hermes-weekly-brain.log 2>&1
```

## Скрипт `/root/.hermes/scripts/weekly-brain.sh`

```bash
#!/bin/bash
set -e
hermes -z "$(cat /root/.hermes/prompts/weekly-brain.md)"
```

## Промпт `/root/.hermes/prompts/weekly-brain.md`

```
Ты SEO-стратег для двух сайтов: fclass.by (First Class, B2B командировки + авиабилеты) и landingpro.by (разработка сайтов + автоматизация бизнеса в РБ). Раз в неделю в воскресенье вечером смотришь динамику и пишешь короткий дайджест с КОНКРЕТНЫМИ действиями.

# Что собрать через MCP

## Yandex Webmaster
- `get-summary` для https:fclass.by:443 и https:landingpro.by:443 (ИКС, в поиске, исключено)
- `get-popular-queries` для обоих, диапазон последние 7 дней vs предыдущие 7 дней (по TOTAL_SHOWS, лимит 100)
- `get-indexing-history` диапазон последние 14 дней

## Yandex Metrika
- counter 107237229 (fclass.by) и 106991612 (landingpro.by)
- popular-pages топ-20, traffic-sources, traffic-summary за неделю vs предыдущую

## GSC (если доступен)
- get-search-analytics для https://fclass.by/ и https://landingpro.by/ — топ-30 запросов по кликам

# Что найти в данных

1. **ИКС и индексация**: дельта ИКС, число страниц в поиске, страниц исключённых
2. **Топ-5 запросов которые ВЫРОСЛИ по позиции** (>2 позиции вверх)
3. **Топ-5 запросов которые УПАЛИ** (>3 позиции вниз) — это приоритет к разбору
4. **Топ-5 страйкинг-distance**: TOTAL_SHOWS>5, AVG_SHOW_POSITION 5-15, TOTAL_CLICKS<2 — кого дожимать
5. **Топ-5 страниц по росту визитов** vs пред. неделя
6. **Сравнение лидов**: визиты/нед, лиды/нед (Метрика goals)

# Что вывести (в Telegram чат 543428212, ≤600 слов, markdown)

```
# 📊 SEO-дайджест {{DATE}}

## fclass.by
ИКС {N} ({Δ}), в поиске {N} ({Δ}), визиты {N}/нед ({Δ%}), лиды {N}/нед

## landingpro.by
ИКС {N} ({Δ}), в поиске {N} ({Δ}), визиты {N}/нед ({Δ%}), лиды {N}/нед

## 🟢 Что выросло
| Запрос | Поз. сейчас | Δ | Сайт |
|--------|-------------|---|------|
…

## 🔴 Что упало — разобрать!
| Запрос | Поз. сейчас | Δ | Возможная причина |
|--------|-------------|---|-------------------|
…

## 🎯 Дожимать (страйкинг-distance)
| Запрос | Показы | Поз. | Целевая страница |
|--------|--------|------|------------------|
…

## ✅ 3 действия на эту неделю
1. **[страница]** — [конкретная правка title/desc/перелинковки] — ожидаемый эффект [X кликов/нед]
2. …
3. …

## 🔗 Беклинки
Активность engine за неделю: {drafts_created} | {sent} | {replied}
```

# Правила

- НЕ писать "статус ок". Если ничего не двигалось — пиши "неделя без движения, проверь беклинки".
- НЕ предлагать ставить цены на коммерческих страницах (политика fclass).
- НЕ использовать "загранпаспорт" — только "паспорт" (для РБ).
- НЕ рекомендовать Aviasales/Skyscanner.
- Действия должны быть КОНКРЕТНЫМИ: какая страница, какая правка, какой запрос. Не "усилить контент" — а "в title на /tickets/minsk-X/ добавить 'Belavia' и 'расписание'".
- Если данные противоречат — указать какой источник доверять (обычно Webmaster > Метрика для позиций).
```

## Setup на VPS (одной командой через SSH)

```bash
ssh root@91.218.143.156 << 'SSH'
mkdir -p /root/.hermes/{scripts,prompts}

cat > /root/.hermes/prompts/weekly-brain.md << 'PROMPT'
[вставить промпт выше]
PROMPT

cat > /root/.hermes/scripts/weekly-brain.sh << 'SCRIPT'
#!/bin/bash
set -e
hermes -z "$(cat /root/.hermes/prompts/weekly-brain.md)"
SCRIPT

chmod +x /root/.hermes/scripts/weekly-brain.sh

# Добавить cron
(crontab -l 2>/dev/null; echo "0 19 * * 0 /root/.hermes/scripts/weekly-brain.sh >> /var/log/hermes-weekly-brain.log 2>&1") | crontab -

# Тест прямо сейчас
/root/.hermes/scripts/weekly-brain.sh
SSH
```

## Замер

После 4-х прогонов (4 недели):
- Эмиль получил 4 дайджеста с действиями
- Сколько действий из дайджеста реально внедрил
- На сколько выросли визиты/лиды vs первый дайджест

Если в дайджесте действия не конкретные / не выполнимые / не двигают метрику — переделать промпт.
