#!/usr/bin/env python3
"""IndexNow ping: tell Bing/Yandex/DuckDuckGo to recrawl 8 new fclass URLs."""
import json, urllib.request, ssl

ctx = ssl.create_default_context()

KEY = "d5ff0dd9bc774d63a8b84e9fd843d23d"
HOST = "fclass.by"
KEY_LOCATION = f"https://{HOST}/indexnow-key.txt"
URLS = [
    "https://fclass.by/komandirovki/",
    "https://fclass.by/tickets/aviabilety-dlya-yurlic/",
    "https://fclass.by/cases/",
    "https://fclass.by/resources/dogovor-template/",
    "https://fclass.by/resources/calculator/",
    "https://fclass.by/tickets/minsk-moskva/",
    "https://fclass.by/tickets/minsk-spb/",
    "https://fclass.by/tickets/minsk-stambul/",
    "https://fclass.by/tickets/minsk-dubai/",
    "https://fclass.by/tickets/minsk-kaliningrad/",
    "https://fclass.by/tickets/minsk-sochi/",
    "https://fclass.by/tickets/minsk-baku/",
    "https://fclass.by/tickets/minsk-tashkent/",
    "https://fclass.by/tickets/minsk-tbilisi/",
    "https://fclass.by/tickets/minsk-sharm-el-sheikh/",
    "https://fclass.by/tickets/minsk-batumi/",
    "https://fclass.by/llms.txt",
    "https://fclass.by/sitemap.xml",
]

payload = {
    "host": HOST,
    "key": KEY,
    "keyLocation": KEY_LOCATION,
    "urlList": URLS,
}
body = json.dumps(payload).encode("utf-8")

# Submit to each search engine's endpoint (they share via IndexNow consortium)
ENDPOINTS = [
    ("api.indexnow.org", "https://api.indexnow.org/IndexNow"),  # generic
    ("yandex.com", "https://yandex.com/indexnow"),  # Yandex direct
    ("bing.com", "https://www.bing.com/indexnow"),  # Bing direct
]

for label, url in ENDPOINTS:
    print(f"\n--- POST {label} ---")
    req = urllib.request.Request(
        url, data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=15)
        print(f"  HTTP {resp.status}  body: {resp.read()[:200]}")
    except urllib.error.HTTPError as e:
        body_e = e.read().decode("utf-8", errors="replace")[:300]
        print(f"  FAIL HTTP {e.code}: {body_e}")
    except Exception as e:
        print(f"  ERROR: {e}")
