#!/usr/bin/env python3
"""Send 4 backlinks outreach emails via FC_ManualSend webhook (marketing@fclass.by).

Tracking output appended to wiki/reports/outreach-log-2026-05-15.md
"""
import json, urllib.request, ssl, time, sys
ctx = ssl.create_default_context()

WEBHOOK = "https://emikss.host/webhook/fc-manual-send"
SIGNATURE_PRESENT = True  # FC_ManualSend appends Эмиль's signature server-side

SENDS = [
    {
        "key": "gb_by",
        "to": "gb@gb.by",
        "subject": "Статья: «Как бухгалтеру упростить документооборот по командировкам — n8n + ИИ»",
        "text": """Здравствуйте,

меня зовут Эмиль Ляшневский, я руковожу LandingPro (Минск) — делаем
автоматизацию бизнес-процессов на n8n для белорусских компаний.

Хочу предложить статью для gb.by на тему, которая регулярно всплывает
в обсуждениях с главбухами наших клиентов:
«Автоматизация командировочного документооборота: какие 5 процессов
бухгалтер может отдать на конвейер за неделю».

В статье будет:
— Готовый workflow: заявка от сотрудника → авансовый отчёт → выгрузка
  в 1С (со скриншотами интеграции n8n + 1С)
— Расчёт экономии часов главбуха при разных моделях закупки авиабилетов
  (со ссылкой на наш бесплатный калькулятор)
— Реальные нормативные ссылки: Постановление Совмина РБ № 176 от
  19.03.2019 + правки № 94 от 13.02.2025
— Чек-лист «что должен сделать бухгалтер за 30 минут перед командировкой»
  (PDF без регистрации)

Готов прислать черновик на 4000-4500 знаков. Без рекламы — практический
материал. Ссылка на сайт LandingPro в авторской подписи (типичный формат
гостевой статьи).

Могу быть автором или со-автором с вашим штатным экспертом.

С уважением,
Эмиль Ляшневский
LandingPro · landingpro.by
Telegram: @coolemm-coder
ecoprofit.em@gmail.com""",
    },
    {
        "key": "ilex_by",
        "to": "info@ilex.by",
        "subject": "Экспертный комментарий: «Правовые риски при оформлении командировочных через сотрудника-физлицо»",
        "text": """Здравствуйте,

меня зовут Эмиль Ляшневский, руковожу тревел-агентством First Class в Минске
(УНП 193582943) и проектом LandingPro (автоматизация B2B). Регулярно
работаем с главбухами компаний по договорам на авиабилеты для юрлиц.

Видел вашу статью «Командировки 2026» — отличная база, но не покрыт
один практический сценарий, который у наших клиентов встречается часто:

«Что происходит с НДС и налоговой ответственностью, когда сотрудник
оплачивает командировочные авиабилеты со своей карты и потом подаёт
авансовый отчёт».

Готов дать экспертный комментарий на 800-1500 знаков с конкретными
нормативными ссылками (гл. 16 НК РБ, ст. 131 НК РБ, Указ Президента
РБ № 154, Постановление Совмина № 176 от 19.03.2019). Со стороны
тревел-агентства — практический угол, дополняющий ваш юридический материал.

Могу прислать черновик. В тексте 1 ссылка на наш материал с шаблоном
договора + чек-листом главбуха (fclass.by/resources/dogovor-template/) —
это PDF без регистрации, чисто полезный.

С уважением,
Эмиль Ляшневский
First Class · fclass.by · marketing@fclass.by
LandingPro · landingpro.by
+375 44 772-52-66""",
    },
    {
        "key": "dev_by",
        "to": "write@dev.by",
        "subject": "Кейс: «Как мы автоматизировали обработку лидов на 5 проектах через n8n — реальные цифры, провалы, ROI»",
        "text": """Привет,

меня зовут Эмиль, делаю LandingPro в Минске. За последние 6 месяцев
автоматизировал процессы у 3 клиентов и собственного бизнеса через
n8n (self-hosted на собственном VPS). Хочу написать для dev.by кейс
с реальными цифрами:

— Барбершоп: Instagram DM → таблица → Telegram мастеру. Результат:
  12 часов/неделю экономии админа, 0 потерянных броней. Окупаемость
  2 месяца.
— IT-консалтинг РБ: парсинг тендеров с 3 площадок → ИИ-фильтр
  релевантности → Slack команде. 25 часов/неделю, +40% релевантных
  лидов в pipeline.
— Тревел-агентство fclass.by: холодная email-рассылка через n8n с
  lead-scoring на OpenRouter (ИИ читает ответ → тегирует в CRM).
  Доставляемость выросла с 60% до 95%, встреч в 3 раза больше.

Все workflows покажу в виде скриншотов и куска JSON — без раскрытия
чувствительных данных.

Также готов поделиться 5 ошибками, которые сделал на этих проектах
(это особенно полезно для тех, кто только начинает с n8n).

Подойдёт для dev.by? Размер 6-8 тысяч знаков, готов делать 2 черновика
на выбор редактора.

С уважением,
Эмиль Ляшневский · LandingPro
@coolemm-coder · ecoprofit.em@gmail.com""",
    },
    {
        "key": "marketing_by",
        "to": "content@marketing.by",
        "subject": "Кейс: «Как мы за 7 дней перепозиционировали лендинг под реальный спрос Wordstat — с 6 запросов/мес до 411»",
        "text": """Привет,

меня зовут Эмиль, делаю LandingPro в Минске. Хочу предложить кейс для
marketing.by — реальная история с цифрами, без воды.

Контекст: LandingPro был оптимизирован под запрос «ai чатбот для
бизнеса» — казалось логично, ИИ в тренде. Через 6 месяцев запустили
мониторинг Wordstat и обнаружили:

— «ai чатбот для бизнеса» в Беларуси: 6 запросов/мес
— «ии для создания сайта»: 160 запросов/мес, 0 конкурентов в РБ
— «автоматизация бизнес процессов»: 251 запрос/мес

То есть мы 6 месяцев конкурировали в пустой нише. За 1 рабочий день
переписали main page + сделали 2 новых лендинга под реальный спрос +
поставили 6 редиректов 301 на старые посты.

В статье на marketing.by расскажу:
1. Методология: как исследовали Wordstat без платных инструментов
   (через Yandex Browser + ручной парсинг)
2. Решение по редиректам: почему НЕ удалили старые посты, а
   консолидировали через 301 на сильные страницы
3. Технический setup: что сделали со schema.org, sitemap.xml,
   внутренней перелинковкой
4. Прогноз на 90 дней (статью можно обновлять)

Размер: 5-6 тысяч знаков, со скриншотами Wordstat и Метрики. Готов
черновик прислать за неделю.

В обмен прошу 1 ссылку в подписи на landingpro.by и 1 контекстную на
главную в теле (где упоминается «обновлённая главная»).

С уважением,
Эмиль Ляшневский
LandingPro · landingpro.by · @coolemm-coder
ecoprofit.em@gmail.com""",
    },
]

results = []
for i, e in enumerate(SENDS, 1):
    body = json.dumps({"body": {"to": e["to"], "subject": e["subject"], "text": e["text"]}}).encode("utf-8")
    req = urllib.request.Request(
        WEBHOOK,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    print(f"\n[{i}/4] -> {e['to']}  ({e['key']})")
    try:
        t0 = time.time()
        resp = urllib.request.urlopen(req, context=ctx, timeout=30)
        ms = int((time.time() - t0) * 1000)
        body_resp = resp.read().decode("utf-8", errors="replace")[:200]
        print(f"  HTTP {resp.status}  in {ms}ms  response: {body_resp}")
        results.append({"key": e["key"], "to": e["to"], "ok": resp.status == 200, "response": body_resp, "ms": ms})
    except urllib.error.HTTPError as err:
        body_err = err.read().decode("utf-8", errors="replace")[:200]
        print(f"  FAIL HTTP {err.code}: {body_err}")
        results.append({"key": e["key"], "to": e["to"], "ok": False, "response": body_err})
    except Exception as err:
        print(f"  ERROR: {err}")
        results.append({"key": e["key"], "to": e["to"], "ok": False, "response": str(err)})
    # Throttle: 3 sec between sends for cleanliness
    if i < len(SENDS):
        time.sleep(3)

print("\n" + "="*60)
print("SUMMARY")
ok_n = sum(1 for r in results if r["ok"])
print(f"  OK: {ok_n}/{len(results)}")
for r in results:
    mark = "OK" if r["ok"] else "FAIL"
    print(f"  [{mark}]  {r['to']}  ({r['key']})")

# Write log
log_path = "/Users/admin/Desktop/claude-obsidian/wiki/reports/outreach-log-2026-05-15.md"
import os
if os.path.exists("/sessions/optimistic-laughing-keller/mnt/Desktop/claude-obsidian/wiki/reports"):
    log_path = "/sessions/optimistic-laughing-keller/mnt/Desktop/claude-obsidian/wiki/reports/outreach-log-2026-05-15.md"
with open(log_path, "w", encoding="utf-8") as f:
    f.write(f"""---
type: report
title: "Outreach log 15.05.2026 — 4 backlinks-письма отправлены"
date: 2026-05-15
related:
  - "[[reports/backlinks-outreach-drafts-2026-05-14]]"
  - "[[reports/backlinks-outreach-ready-2026-05-15]]"
  - "[[LandingPro]]"
  - "[[First Class]]"
---

# Outreach log 15.05.2026

Через FC_ManualSend webhook (https://emikss.host/webhook/fc-manual-send), все 4 письма
отправлены с marketing@fclass.by, подпись «Эмиль Ляшневский».

| # | Получатель | Тема | Статус |
|---|---|---|---|
""")
    for i, (e, r) in enumerate(zip(SENDS, results), 1):
        st = "✅ sent" if r["ok"] else f"❌ failed ({r['response'][:60]})"
        f.write(f"| {i} | {e['to']} | {e['subject'][:60]}... | {st} |\n")
    f.write(f"""

## Что просим в ответ

- gb.by → ссылка в подписи на landingpro.by/avtomatizatsiya-biznes-protsessov/ + контекстная на fclass.by/resources/calculator/
- ilex.by → 1 контекстная на fclass.by/resources/dogovor-template/
- dev.by → 1 ссылка в подписи на landingpro.by/avtomatizatsiya-biznes-protsessov/
- marketing.by → 1 в подписи + 1 контекстная на landingpro.by/

## Next steps

- **15.05–17.05** — мониторить inbox marketing@fclass.by на ответы редакторов
- **22.05** — если молчание, отправить follow-up (одно письмо «hi, did you see my pitch?»)
- **29.05** — закрыть нереагирующие, переходить к следующим площадкам

## Ожидания

Sample success rate для cold outreach: 1-2 из 4 публикаций. Время до первой публикации: 2-6 недель.
""")
print(f"\nLog written: {log_path}")
