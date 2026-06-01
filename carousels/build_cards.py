#!/usr/bin/env python3
"""Build FC single-post cards: snap-deal + lowcost. 1080x1350 (4:5)."""
import json
import base64
from pathlib import Path

BASE = Path(__file__).parent
brand = json.loads((BASE / "brand-config.json").read_text())
ACCENT = brand["accent_color"]
HANDLE = brand["handle"]
BG_DARK = "#0c1825"
TEXT = "#ffffff"
MUTED = "#8a99ac"

LOGO_PATH = BASE.parent / "logo.png"
LOGO_B64 = ("data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode()
            if LOGO_PATH.exists() else "")


def bg_uri(name):
    p = BASE / "bg" / f"{name}.jpg"
    if not p.exists() or p.stat().st_size < 5000:
        return ""
    head = p.read_bytes()[:8]
    mime = "image/png" if head.startswith(b"\x89PNG") else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


CSS = f'''
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#222;display:flex;gap:24px;padding:40px;flex-wrap:wrap;justify-content:center;font-family:'Poppins',sans-serif}}
.card{{width:420px;height:525px;position:relative;overflow:hidden;color:{TEXT};flex-shrink:0}}
.overlay{{position:absolute;inset:0;background:linear-gradient(rgba(12,24,37,.62),rgba(12,24,37,.92))}}
.logo-img{{position:absolute;top:28px;left:28px;height:34px;z-index:5}}
.tag{{position:absolute;top:34px;right:28px;z-index:5;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:{ACCENT};border:1px solid {ACCENT};padding:6px 14px;border-radius:30px}}
.body{{position:absolute;bottom:90px;left:32px;right:32px;z-index:5}}
.route{{font-family:'Playfair Display',serif;font-size:44px;font-weight:700;line-height:1.05;letter-spacing:-.5px}}
.route .arr{{color:{ACCENT}}}
.meta{{font-size:16px;color:{TEXT};margin-top:10px;font-weight:500}}
.price-row{{display:flex;align-items:baseline;gap:10px;margin-top:18px}}
.price{{font-size:54px;font-weight:800;color:{ACCENT};line-height:1}}
.price-cur{{font-size:22px;font-weight:700;color:{ACCENT}}}
.note{{font-size:15px;font-style:italic;color:{MUTED};margin-top:12px;line-height:1.45;max-width:340px}}
.foot{{position:absolute;bottom:30px;left:32px;right:32px;z-index:5;display:flex;justify-content:space-between;align-items:center;border-top:1px solid rgba(255,255,255,.15);padding-top:14px}}
.foot .ph{{font-size:15px;font-weight:700;color:{ACCENT}}}
.foot .hd{{font-size:12px;color:{MUTED}}}
'''


def snap_deal(bg, tag, frm, to, meta, price, cur, note):
    img = bg_uri(bg)
    bgstyle = (f"background:url('{img}');background-size:cover;background-position:center"
               if img else f"background:{BG_DARK}")
    return f'''
  <div class="card" style="{bgstyle}">
    <div class="overlay"></div>
    {f'<img src="{LOGO_B64}" class="logo-img">' if LOGO_B64 else ''}
    <div class="tag">{tag}</div>
    <div class="body">
      <div class="route">{frm} <span class="arr">→</span><br>{to}</div>
      <div class="meta">{meta}</div>
      <div class="price-row"><span class="price">{price}</span><span class="price-cur">{cur}</span></div>
      <div class="note">{note}</div>
    </div>
    <div class="foot"><span class="ph">+375 44 772-52-66</span><span class="hd">{HANDLE}</span></div>
  </div>'''


cards = [
    # SNAP-DEAL
    snap_deal("istanbul", "Прямой рейс", "МИНСК", "СТАМБУЛ",
              "12 июня · Belavia · 2 ч в пути",
              "230", "BYN",
              "Места есть. Оформим за 10 минут — звоните или пишите в личку."),
    # LOWCOST
    snap_deal("barcelona", "Лоукост", "ВИЛЬНЮС", "БАРСЕЛОНА",
              "Wizz Air · 18 июня · из Вильнюса",
              "47", "EUR",
              "Wizz не принимает карты РБ? Выкупим за вас + трансфер Минск→Вильнюс. Пакет ~250 BYN."),
]

html = f'''<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<title>FC Cards</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{"".join(cards)}
</body></html>'''

out = BASE / "2026" / "05" / "cards-snap-lowcost.html"
out.write_text(html, encoding="utf-8")
print(f"OK: {out} ({len(cards)} cards)")
