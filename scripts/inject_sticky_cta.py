#!/usr/bin/env python3
"""Inject sticky-mobile-cta on 5 B2B pages.

Each page already has .tg-bubble. We add a sticky bar at the bottom
with click-to-call + Telegram. Uses media (max-width:768px) to show only on mobile.
"""
import os, re

PAGES = [
    ("komandirovki/index.html", "lead_komandirovki_mobile"),
    ("tickets/aviabilety-dlya-yurlic/index.html", "lead_yurlic_mobile"),
    ("resources/calculator/index.html", "lead_calc_mobile"),
    ("resources/dogovor-template/index.html", "lead_dogovor_mobile"),
    ("cases/index.html", "lead_cases_mobile"),
]

# Auto-detect root
ROOTS = ("/sessions/optimistic-laughing-keller/mnt/Desktop/FirstClass_Automation",
         "/Users/admin/Desktop/FirstClass_Automation")
ROOT = next(r for r in ROOTS if os.path.isdir(r))

# CSS (shared, kept compact)
CSS = """
.sticky-mobile-cta{display:none;position:fixed;bottom:0;left:0;right:0;z-index:99;padding:12px 16px;background:rgba(255,255,255,.95);backdrop-filter:blur(8px);border-top:1px solid rgba(0,0,0,.08);gap:8px}
@media(max-width:768px){.sticky-mobile-cta{display:flex}.tg-bubble{bottom:80px}}
.sticky-mobile-cta a{flex:1;text-align:center;padding:12px;border-radius:8px;font-weight:600;font-size:14px;text-decoration:none}
.sticky-mobile-cta .smc-call{background:#c9a962;color:#fff}
.sticky-mobile-cta .smc-tg{background:#f1f5f9;color:#1e293b}
"""

def html_block(tg_param):
    return f'''<div class="sticky-mobile-cta">
    <a href="tel:+375447725266" class="smc-call" onclick="try{{ym(107237229,'reachGoal','sticky_call_{tg_param}');}}catch(e){{}}">Позвонить</a>
    <a href="https://t.me/travelangelby_bot?start=sticky_{tg_param}" class="smc-tg" target="_blank" rel="noopener" onclick="try{{ym(107237229,'reachGoal','sticky_tg_{tg_param}');}}catch(e){{}}">Telegram</a>
</div>'''

for page, tg in PAGES:
    fp = f"{ROOT}/{page}"
    with open(fp, encoding="utf-8") as f:
        s = f.read()
    orig = s

    # Idempotency check
    if 'class="sticky-mobile-cta"' in s:
        print(f"  SKIP (already has sticky-mobile-cta): {page}")
        continue

    # Inject CSS — append to last <style> block before </head>
    # find the </style> right before </head>
    head_idx = s.find("</head>")
    if head_idx == -1:
        print(f"  FAIL — no </head> in {page}")
        continue
    # find last </style> before </head>
    style_end_idx = s.rfind("</style>", 0, head_idx)
    if style_end_idx == -1:
        print(f"  FAIL — no </style> before </head> in {page}")
        continue
    s = s[:style_end_idx] + CSS + s[style_end_idx:]

    # Inject HTML before </body>
    body_idx = s.rfind("</body>")
    if body_idx == -1:
        print(f"  FAIL — no </body> in {page}")
        continue
    block = html_block(tg) + "\n"
    s = s[:body_idx] + block + s[body_idx:]

    with open(fp, "w", encoding="utf-8") as f:
        f.write(s)
    print(f"  OK: {page}  ({len(s) - len(orig):+d} chars)")

print("\n=== sanity check — sticky-mobile-cta count ===")
for page, _ in PAGES:
    fp = f"{ROOT}/{page}"
    with open(fp, encoding="utf-8") as f:
        s = f.read()
    cnt_class = s.count('class="sticky-mobile-cta"')
    cnt_css = s.count('.sticky-mobile-cta{')
    print(f"  {page}: HTML={cnt_class}, CSS={cnt_css}")
