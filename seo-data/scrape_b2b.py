import subprocess, re, sys, time, urllib.parse, os, csv, datetime
STATE=os.path.expanduser("~/.agent-browser/yandex-wordstat.json")
AB=os.path.expanduser("~/.npm-global/bin/agent-browser")
REGION=149
KW=[
 "авиабилеты для бизнеса","авиабилеты для компании","авиабилеты с ндс",
 "корпоративные авиабилеты","деловые поездки","деловая поездка за границу",
 "организация поездки на выставку","командировка на выставку","поездка на выставку 2026",
 "корпоративная поездка","mice беларусь","бизнес тур","выставки 2026","авиабилеты оптом",
]
def scrape(kw):
    url=f"https://wordstat.yandex.ru/?words={urllib.parse.quote(kw)}&region={REGION}"
    try:
        subprocess.run([AB,"--state",STATE,"open",url],capture_output=True,text=True,timeout=60)
        time.sleep(2)
        snap=subprocess.run([AB,"snapshot"],capture_output=True,text=True,timeout=60).stdout
    except Exception: return None
    m=re.search(r"за[^:]*:\s*([\d  ]+)",snap)
    if m:
        dg=re.sub(r"\D","",m.group(1)); return int(dg) if dg else None
    return None
for kw in KW:
    v=scrape(kw)
    print(f"  {v if v is not None else 'н/д':>7}  {kw}", flush=True)
