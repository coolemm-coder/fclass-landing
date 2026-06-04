#!/usr/bin/env python3
"""Google Autocomplete scraper — направление спроса Google (что вводят пользователи).
Бесплатно, без логина. НЕ объёмы (для абсолютных нужен Keyword Planner + Google Ads).
Использует curl (python-SSL на маке сломан). Пишет google-suggest.csv.
Дополняет: Yandex Wordstat (абс. объёмы) + GSC (где FC ранжируется)."""
import subprocess, json, csv, sys, datetime, os, urllib.parse
OUT=os.path.expanduser("~/Desktop/FirstClass_Automation/seo-data/google-suggest.csv")
SEEDS=[
 "авиабилеты для","авиабилеты минск","авиабилеты по","билеты для","билеты на самолет для",
 "командировка в","командировка на","командировка за","организация командировок","деловая поездка",
 "авиабилеты бизнес","выставка 2026","поездка на выставку","корпоративные авиабилеты","авиабилеты юр",
]
def sug(q):
    u="https://suggestqueries.google.com/complete/search?"+urllib.parse.urlencode(
        {"client":"chrome","hl":"ru","gl":"by","q":q})
    try:
        out=subprocess.run(["curl","-s","-H","User-Agent: Mozilla/5.0","--max-time","12",u],
                           capture_output=True,text=True,timeout=20).stdout
        d=json.loads(out); return d[1] if len(d)>1 else []
    except Exception: return []
def main():
    today=datetime.date.today().isoformat(); rows=[]
    for seed in SEEDS:
        s=sug(seed)
        print(f"  {seed} -> {len(s)}")
        for q in s: rows.append([today,seed,q])
    new=not os.path.exists(OUT)
    with open(OUT,"a",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        if new: w.writerow(["date","seed","suggestion"])
        w.writerows(rows)
    print(f"\n✓ {len(rows)} строк → {OUT}")
if __name__=="__main__": main()
