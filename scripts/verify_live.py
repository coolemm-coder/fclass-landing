#!/usr/bin/env python3
import urllib.request, ssl, re
ctx = ssl.create_default_context()

URLS = [
    "https://fclass.by/",
    "https://fclass.by/komandirovki/",
    "https://fclass.by/tickets/aviabilety-dlya-yurlic/",
    "https://fclass.by/resources/dogovor-template/",
    "https://fclass.by/resources/calculator/",
    "https://fclass.by/cases/",
    "https://fclass.by/sitemap.xml",
    "https://fclass.by/blog/korporativnye-aviabilety-minsk.html",
    "https://landingpro.by/",
]

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"

def head(url):
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        r = urllib.request.urlopen(req, context=ctx, timeout=8)
        return r.status, r.headers.get("Content-Length", "?")
    except urllib.error.HTTPError as e:
        return e.code, "?"
    except Exception as e:
        return "ERR", str(e)[:60]

print("=== Live HTTP checks ===")
for u in URLS:
    code, ln = head(u)
    print(f"  {code:>3}  size={ln}  {u}")

print()
print("=== Forbidden terms check (komandirovki + aviabilety-dlya-yurlic) ===")
forbidden = [
    r"15-25%", r"10-25%", r"15-20%",
    r"корпоративный договор",
    r"турагентство",
    r"Окупаемость 1-2",
    r"НДС автоматически",
    r"отсрочк[аеои][^ ]* 7 дн",
    r"отсрочк[аеои][^ ]* 14 дн",
    r"отсрочк[аеои][^ ]* 30 дн",
]
for u in ["https://fclass.by/komandirovki/", "https://fclass.by/tickets/aviabilety-dlya-yurlic/"]:
    body = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), context=ctx, timeout=8).read().decode("utf-8", errors="replace")
    hits = []
    for p in forbidden:
        for m in re.finditer(p, body):
            hits.append(m.group(0))
    if hits:
        print(f"  DIRTY {u}  ->  {set(hits)}")
    else:
        print(f"  CLEAN {u}")
