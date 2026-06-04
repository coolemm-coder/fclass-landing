#!/usr/bin/env python3
"""РБ-радар Wordstat для fclass: скрейпит спрос по ключам через сохранённую сессию agent-browser."""
import subprocess, re, csv, sys, time, urllib.parse, datetime, os

STATE = os.path.expanduser("~/.agent-browser/yandex-wordstat.json")
REGION = 149  # Беларусь
OUT = os.path.expanduser("~/Desktop/FirstClass_Automation/seo-data/wordstat-rb.csv")
AB = os.path.expanduser("~/.npm-global/bin/agent-browser")

KEYWORDS = [
    # B2B / коммерция
    "организация командировок", "авиабилеты для юрлиц", "командировки минск",
    # маршруты
    "авиабилеты минск батуми", "авиабилеты минск стамбул", "прямые рейсы из минска",
    "авиабилеты минск москва", "минск тбилиси авиабилеты",
    "авиабилеты для юридических лиц", "авиабилеты по безналу",
    # маршруты — мультикарьер / выбор (угол FC)
    "авиабилеты минск дубай", "авиабилеты минск баку", "авиабилеты минск ташкент",
    "авиабилеты минск ереван", "авиабилеты минск пекин",
    # чартер / море
    "авиабилеты минск анталья", "авиабилеты минск хургада", "авиабилеты минск шарм-эль-шейх",
    # Европа — только стыковки (прямых нет с 2021, сильный угол FC)
    "авиабилеты в европу из минска", "авиабилеты минск прага",
    # РФ доп
    "авиабилеты минск санкт-петербург", "авиабилеты минск сочи",
    # премиум
    "авиабилеты бизнес класс минск",
    # суточные / командировочные
    "суточные 2026", "командировочные рб 2026", "суточные в россию из беларуси",
    # визы
    "шенгенская виза для белорусов", "виза в китай для белорусов",
    "консульский сбор шенген", "виза в калининград для белорусов",
]

def scrape(kw):
    url = f"https://wordstat.yandex.ru/?words={urllib.parse.quote(kw)}&region={REGION}"
    try:
        subprocess.run([AB, "--state", STATE, "open", url], capture_output=True, text=True, timeout=60)
        time.sleep(2)
        snap = subprocess.run([AB, "snapshot"], capture_output=True, text=True, timeout=60).stdout
    except Exception as e:
        return None
    m = re.search(r"за[^:]*:\s*([\d  ]+)", snap)
    if m:
        digits = re.sub(r"\D", "", m.group(1))
        return int(digits) if digits else None
    return None

def main(limit=None):
    kws = KEYWORDS[:limit] if limit else KEYWORDS
    today = datetime.date.today().isoformat()
    rows = []
    for kw in kws:
        v = scrape(kw)
        print(f"  {v if v is not None else 'н/д':>7}  {kw}")
        rows.append([today, kw, REGION, v if v is not None else ""])
    new = not os.path.exists(OUT)
    with open(OUT, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "keyword", "region", "volume"])
        w.writerows(rows)
    print(f"\n✓ записано {len(rows)} строк → {OUT}")

if __name__ == "__main__":
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else None
    main(lim)
