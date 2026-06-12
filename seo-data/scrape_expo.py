import subprocess, re, sys, time, urllib.parse, os
STATE=os.path.expanduser("~/.agent-browser/yandex-wordstat.json"); AB=os.path.expanduser("~/.npm-global/bin/agent-browser"); REGION=149
KW=[
 # календарь/гео
 "выставки 2026","выставки москва 2026","выставки в китае 2026","выставки дубай","выставки европа 2026",
 # травел-интент
 "командировка на выставку","поездка на выставку","билеты на выставку",
 # конкретные крупные (что едут бел-компании)
 "кантонская выставка 2026","иннопром 2026","gitex 2026","gulfood 2026","arab health 2026",
 "продэкспо 2026","agritechnica 2026","выставка в москве 2026","ligna 2026","big 5 dubai",
]
def scrape(kw):
    url=f"https://wordstat.yandex.ru/?words={urllib.parse.quote(kw)}&region={REGION}"
    try:
        subprocess.run([AB,"--state",STATE,"open",url],capture_output=True,text=True,timeout=60); time.sleep(2)
        snap=subprocess.run([AB,"snapshot"],capture_output=True,text=True,timeout=60).stdout
    except Exception: return None
    m=re.search(r"за[^:]*:\s*([\d  ]+)",snap)
    if m:
        dg=re.sub(r"\D","",m.group(1)); return int(dg) if dg else None
    return None
for kw in KW:
    v=scrape(kw); print(f"  {v if v is not None else 'н/д':>7}  {kw}", flush=True)
