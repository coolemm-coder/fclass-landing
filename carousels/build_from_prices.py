#!/usr/bin/env python3
"""Generate FC price cards from prices.json (manager-updated, no API).
Each route -> 1 card (1080x1350). Price shown as «от X» (orientir, not offer)."""
import json
import base64
from pathlib import Path

BASE = Path(__file__).parent
brand = json.loads((BASE / "brand-config.json").read_text())
data = json.loads((BASE / "prices.json").read_text())
ACCENT = brand["accent_color"]
HANDLE = brand["handle"]
BG_DARK = "#0c1825"
TEXT = "#ffffff"
MUTED = "#8a99ac"

LOGO_PATH = BASE.parent / "logo.png"
LOGO_B64 = ("data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode()
            if LOGO_PATH.exists() else "")


def bg_uri(name):
    if not name:
        return ""
    p = BASE / "bg" / f"{name}.jpg"
    if not p.exists() or p.stat().st_size < 5000:
        return ""
    head = p.read_bytes()[:8]
    mime = "image/png" if head.startswith(b"\x89PNG") else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def card(r):
    img = bg_uri(r.get("bg", ""))
    bgstyle = (f"background:url('{img}');background-size:cover;background-position:center"
               if img else f"background:{BG_DARK}")
    is_low = r.get("type") == "lowcost"
    tag = "Лоукост" if is_low else "Прямой рейс"
    note = (f"Wizz не принимает карты РБ? Выкупим за вас + трансфер из Минска. Точную цену и пакет считает менеджер."
            if is_low else
            f"Цена-ориентир на ближайшие даты. Точную стоимость под ваши даты считает менеджер.")
    return f'''
  <div class="card" style="{bgstyle}">
    <div class="overlay"></div>
    {f'<img src="{LOGO_B64}" class="logo-img">' if LOGO_B64 else ''}
    <div class="tag">{tag}</div>
    <div class="body">
      <div class="route">{r['from']} <span class="arr">→</span><br>{r['to']}</div>
      <div class="meta">{r['airline']}</div>
      <div class="price-row"><span class="ot">от</span><span class="price">{r['price']}</span><span class="price-cur">{r['cur']}</span></div>
      <div class="note">{note}</div>
    </div>
    <div class="foot"><span class="ph">+375 44 772-52-66</span><span class="hd">{HANDLE}</span></div>
  </div>'''


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#222;display:flex;gap:24px;padding:40px;flex-wrap:wrap;justify-content:center;font-family:'Poppins',sans-serif}}
.card{{width:420px;height:525px;position:relative;overflow:hidden;color:{TEXT};flex-shrink:0}}
.overlay{{position:absolute;inset:0;background:linear-gradient(rgba(12,24,37,.6),rgba(12,24,37,.92))}}
.logo-img{{position:absolute;top:28px;left:28px;height:34px;z-index:5}}
.tag{{position:absolute;top:34px;right:28px;z-index:5;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:{ACCENT};border:1px solid {ACCENT};padding:6px 14px;border-radius:30px}}
.body{{position:absolute;bottom:90px;left:32px;right:32px;z-index:5}}
.route{{font-family:'Playfair Display',serif;font-size:44px;font-weight:700;line-height:1.05;letter-spacing:-.5px}}
.route .arr{{color:{ACCENT}}}
.meta{{font-size:16px;color:{TEXT};margin-top:10px;font-weight:500}}
.price-row{{display:flex;align-items:baseline;gap:8px;margin-top:18px}}
.ot{{font-size:20px;color:{MUTED};font-weight:600}}
.price{{font-size:54px;font-weight:800;color:{ACCENT};line-height:1}}
.price-cur{{font-size:22px;font-weight:700;color:{ACCENT}}}
.note{{font-size:14px;font-style:italic;color:{MUTED};margin-top:12px;line-height:1.4;max-width:345px}}
.foot{{position:absolute;bottom:30px;left:32px;right:32px;z-index:5;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,.15);padding-top:14px}}
.foot .ph{{font-size:15px;font-weight:700;color:{ACCENT}}}
.foot .hd{{font-size:12px;color:{MUTED}}}
'''

cards = "".join(card(r) for r in data["routes"])
html = f'''<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8"><title>FC Price Cards</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{cards}</body></html>'''

out = BASE / "2026" / "05" / "cards-from-prices.html"
out.write_text(html, encoding="utf-8")
print(f"OK: {out} — {len(data['routes'])} карточек из prices.json (обновлено {data['updated']})")
