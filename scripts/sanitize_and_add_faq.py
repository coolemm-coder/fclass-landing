#!/usr/bin/env python3
"""C-2: Sanitize «корпоративн* договор» on resource pages + inject FAQPage JSON-LD."""
import re, sys

import os
# Auto-detect: sandbox mount vs host
for candidate in ("/sessions/optimistic-laughing-keller/mnt/Desktop/FirstClass_Automation",
                  "/Users/admin/Desktop/FirstClass_Automation"):
    if os.path.isdir(candidate):
        ROOT = candidate
        break
else:
    raise SystemExit("ROOT not found")

# --- 1. Replacements per page (keep PDF/H1 title where it's the document's nomenclature,
#       neutralize marketing copy) ---
REPLACEMENTS_DOGOVOR = [
    # JSON-LD: name + description (used by search engines for product identification)
    ("Шаблон корпоративного договора на авиабилеты + чек-лист главбуха",
     "Шаблон договора на авиабилеты для юрлиц + чек-лист главбуха"),
    ('"description":"Готовый шаблон корпоративного договора на авиабилеты для юр.лица в Беларуси',
     '"description":"Готовый шаблон договора на авиабилеты для юрлиц в Беларуси'),
    # H1
    ("<h1>Шаблон корпоративного договора на авиабилеты + чек-лист главбуха</h1>",
     "<h1>Шаблон договора на авиабилеты для юрлиц + чек-лист главбуха</h1>"),
    # H3 «Часть 1»
    ("<h3>Часть 1. Шаблон корпоративного договора</h3>",
     "<h3>Часть 1. Шаблон договора с агентством на авиабилеты для юрлиц</h3>"),
    # Reference link
    ("Подробнее о практике применения корпоративного договора — в",
     "Подробнее о практике работы по договору с агентством на авиабилеты — в"),
    ("«Корпоративный договор на авиабилеты в Минске»",
     "«Договор на авиабилеты для юрлиц в Минске»"),
]

REPLACEMENTS_CALC = [
    ("<h1>Сколько ваша компания экономит с корпоративным договором на авиабилеты</h1>",
     "<h1>Сколько ваша компания экономит с договором на авиабилеты для юрлиц</h1>"),
]

# --- 2. FAQPage schemas to inject ---

FAQ_DOGOVOR = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Что входит в этот PDF?","acceptedAnswer":{"@type":"Answer","text":"Готовый шаблон договора на авиабилеты для юрлиц (9 разделов), пошаговый чек-лист главбуха по командировочным документам и подборка нормативных актов РБ — Постановление Совмина №176, Указ №154, гл.16 НК РБ, ст.131 НК РБ, Закон о защите персональных данных."}},{"@type":"Question","name":"Можно ли использовать этот шаблон с другим агентством?","acceptedAnswer":{"@type":"Answer","text":"Да. Шаблон универсальный — реквизиты исполнителя пустые, заполняются под любого выбранного агента или поставщика. Образец практический, основан на стандартной B2B-практике в Беларуси."}},{"@type":"Question","name":"Этот шаблон легитимный с точки зрения законодательства Беларуси?","acceptedAnswer":{"@type":"Answer","text":"Шаблон опирается на действующие нормативные акты Республики Беларусь: Постановление Совмина №176 (служебные командировки в РБ), Постановление Совмина №94 (командировки за границу), Указ Президента №154, главу 16 Налогового кодекса РБ (НДС), статью 131 НК РБ (расходы на командировки), Закон о защите персональных данных 2021 года. Перед подписанием рекомендуем согласовать с вашим юристом."}},{"@type":"Question","name":"Сколько действует этот документ?","acceptedAnswer":{"@type":"Answer","text":"Документ актуален на 2026 год. Если изменятся нормативные акты — обновим версию и пришлём подписчикам по e-mail."}},{"@type":"Question","name":"Это бесплатно?","acceptedAnswer":{"@type":"Answer","text":"Да. Скачивание PDF бесплатно — нужно только указать e-mail, чтобы мы могли уведомить вас об обновлениях. Не передаём адрес третьим лицам."}}]}</script>'''

FAQ_CALC = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Как считается экономия?","acceptedAnswer":{"@type":"Answer","text":"Калькулятор сравнивает три параметра: количество командировок в месяц, среднюю стоимость пакета (билет + отель + трансфер) и часы сотрудников, которые сейчас тратятся на самостоятельное оформление. Результат — экономия в BYN/год и в часах бухгалтера. Цифры ориентировочные, для точного расчёта менеджер подберёт условия под профиль вашей компании."}},{"@type":"Question","name":"Какие данные нужны для расчёта?","acceptedAnswer":{"@type":"Answer","text":"Три числа: командировок в месяц (целое число), средний бюджет одной поездки (BYN), часов бухгалтера на оформление одной поездки (число). Если не знаете точно — используйте типичные значения по вашей отрасли, калькулятор подскажет диапазон."}},{"@type":"Question","name":"Расчёт включает скидку от агентства?","acceptedAnswer":{"@type":"Answer","text":"Нет. Калькулятор показывает экономию только на сокращении часов сотрудников и на эффективности подбора через GDS. Условия по агентскому вознаграждению и пакету услуг согласуем заранее на этапе подписания договора для юрлиц."}},{"@type":"Question","name":"Можно получить расчёт по моей компании?","acceptedAnswer":{"@type":"Answer","text":"Да. После расчёта в калькуляторе оставьте email — менеджер пришлёт персональное предложение с учётом профиля вашей компании, частоты поездок и направлений."}}]}</script>'''

FAQ_CASES = '''<script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":"Эти кейсы реальные?","acceptedAnswer":{"@type":"Answer","text":"Да. Кейсы основаны на работе с действующими клиентами First Class. Названия компаний и точные цифры по бюджетам анонимизированы по соглашению о конфиденциальности — но методология, объёмы и порядок результатов воспроизводят реальные проекты."}},{"@type":"Question","name":"Сколько занимает запуск работы с First Class?","acceptedAnswer":{"@type":"Answer","text":"Стандартный срок: 5–7 рабочих дней от первого контакта до первой командировки. Сюда входит знакомство с потребностями компании, согласование условий, подписание договора с юрлицами и подключение менеджера. Срочные командировки можем обработать в течение того же рабочего дня."}},{"@type":"Question","name":"Можно ли получить рекомендацию от действующего клиента?","acceptedAnswer":{"@type":"Answer","text":"Да. По запросу подбираем клиента из вашей отрасли с похожим объёмом и связываем напрямую — для прямого разговора без посредников. Контакты передаём только после взаимного согласия."}},{"@type":"Question","name":"Что если в нашей компании командировок мало?","acceptedAnswer":{"@type":"Answer","text":"Работаем и с компаниями, у которых 1–3 командировки в месяц. Условия в этом случае гибче — обсуждаем формат заранее. Для малого объёма часто выгоднее точечные заявки без рамочного договора."}}]}</script>'''

def patch_file(path, replacements, faq_schema):
    with open(path, encoding="utf-8") as f:
        s = f.read()
    orig_len = len(s)
    # 1. Replacements
    for old, new in replacements:
        if old not in s:
            print(f"  WARN: not found in {path}: {old[:60]}")
        else:
            s = s.replace(old, new)
    # 2. Inject FAQ Schema before </head>
    if faq_schema in s:
        print(f"  Already has FAQ schema: {path}")
    else:
        marker = "</head>"
        if marker not in s:
            print(f"  FATAL: no </head> in {path}"); return
        s = s.replace(marker, f"    {faq_schema}\n</head>", 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"  {path}: {orig_len} -> {len(s)} chars (delta {len(s)-orig_len:+d})")

print("=== Patching dogovor-template ===")
patch_file(f"{ROOT}/resources/dogovor-template/index.html", REPLACEMENTS_DOGOVOR, FAQ_DOGOVOR)
print("=== Patching calculator ===")
patch_file(f"{ROOT}/resources/calculator/index.html", REPLACEMENTS_CALC, FAQ_CALC)
print("=== Patching cases ===")
patch_file(f"{ROOT}/cases/index.html", [], FAQ_CASES)

# Sanity check
print("\n=== Sanity check ===")
for f in ["resources/dogovor-template/index.html", "resources/calculator/index.html", "cases/index.html"]:
    with open(f"{ROOT}/{f}", encoding="utf-8") as fp:
        s = fp.read()
    bad = re.findall(r"корпоративн[а-яё]+ договор", s)
    faq_count = s.count('"@type":"FAQPage"')
    print(f"  {f}: bad terms={len(bad)} {('('+ ', '.join(set(bad)) + ')') if bad else ''} | FAQPage blocks={faq_count}")
