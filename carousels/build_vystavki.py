#!/usr/bin/env python3
"""Build FC carousel: 5 exhibitions autumn 2026. Bold Impact style, FC brand."""
import json
import base64
from pathlib import Path

BASE = Path(__file__).parent
brand = json.loads((BASE / "brand-config.json").read_text())
ACCENT = brand["accent_color"]   # #c9a962 gold
HANDLE = brand["handle"]
NAME = brand["name"]
SUB = brand["subtitle"]
INITIALS = brand["initials"]

# Real FC logo (240x80, white-on-transparent for dark backgrounds)
LOGO_PATH = BASE.parent / "logo.png"
LOGO_B64 = ""
if LOGO_PATH.exists():
    LOGO_B64 = "data:image/png;base64," + base64.b64encode(LOGO_PATH.read_bytes()).decode()

BG_ODD = "#0c1825"
BG_EVEN = "#101d32"
TEXT = "#ffffff"
MUTED = "#8a99ac"

# (number, title, place+date, industry, who, bg_image_filename)
EXHIBITIONS = [
    ("01", "ANUGA", "Кёльн · 10–14 октября", "Пищевая промышленность",
     "Крупнейшая в Европе. Раз в 2 года — следующая в 2028.", "cologne.jpg"),
    ("02", "GITEX", "Дубай · октябрь", "IT и технологии",
     "Крупнейшая IT-выставка Ближнего Востока. Безвиз + прямой рейс.", "dubai.jpg"),
    ("03", "CIIE", "Шанхай · 5–10 ноября", "Экспорт в Китай",
     "China Import Expo — выход на рынок КНР с господдержкой.", "shanghai.jpg"),
    ("04", "MEDICA", "Дюссельдорф · 16–20 ноября", "Медицина и фарма",
     "Крупнейшая в мире медицинская выставка.", "dusseldorf.jpg"),
    ("05", "THE BIG 5", "Дубай · 24–27 ноября", "Строительство",
     "Главная стройвыставка GCC. Стройматериалы, оборудование.", "dubai.jpg"),
]


def bg_data_uri(filename):
    """Return base64 data URI for a bg image, or empty if missing/invalid."""
    if not filename:
        return ""
    p = BASE / "bg" / filename
    if not p.exists() or p.stat().st_size < 5000:  # skip tiny/404 files
        return ""
    head = p.read_bytes()[:8]
    is_png = head.startswith(b"\x89PNG")
    is_jpg = head.startswith(b"\xff\xd8\xff")
    if not (is_png or is_jpg):
        return ""
    mime = "image/png" if is_png else "image/jpeg"
    return f"data:{mime};base64," + base64.b64encode(p.read_bytes()).decode()


def profile_header():
    if LOGO_B64:
        logo = f'<img src="{LOGO_B64}" class="logo-img" alt="First Class">'
    else:
        logo = f'<div class="avatar">{INITIALS}</div>'
    return f'''
    <div class="profile">
      {logo}
      <div class="profile-text">
        <div class="psub">{SUB}</div>
      </div>
    </div>'''


def progress_bar(idx, total):
    segs = "".join(
        f'<div class="seg {"on" if i <= idx else ""}"></div>' for i in range(total)
    )
    return f'<div class="progress">{segs}</div>'


def watermark():
    return f'<div class="watermark">{HANDLE}</div>'


def arrow():
    return '<div class="arrow">→</div>'


def hero_slide(total):
    return f'''
  <div class="slide hero" style="background:{BG_ODD}">
    {profile_header()}
    <div class="hero-body">
      <div class="kicker">ОСЕНЬ 2026</div>
      <h1>5 международных <span class="acc">выставок</span> для вашего бизнеса</h1>
      <p class="hero-sub">Куда поехать компании из Беларуси, чтобы найти партнёров и контракты</p>
    </div>
    {watermark()}{arrow()}{progress_bar(0, total)}
  </div>'''


def exhibition_slide(num, title, place, industry, who, bg_file, idx, total):
    bg = BG_ODD if idx % 2 == 0 else BG_EVEN
    img = bg_data_uri(bg_file)
    if img:
        # Photo + dark gradient overlay so text stays readable
        bg_style = (f"background:linear-gradient(rgba(12,24,37,.72),rgba(12,24,37,.94)),"
                    f"url('{img}');background-size:cover;background-position:center")
    else:
        bg_style = f"background:{bg}"
    return f'''
  <div class="slide" style="{bg_style}">
    {profile_header()}
    <div class="ex-body">
      <div class="ex-num">{num}</div>
      <h2 class="ex-title">{title}</h2>
      <div class="ex-place">{place}</div>
      <div class="ex-industry">{industry}</div>
      <p class="ex-who">{who}</p>
    </div>
    {watermark()}{arrow()}{progress_bar(idx, total)}
  </div>'''


def cta_slide(idx, total):
    return f'''
  <div class="slide cta" style="background:{BG_ODD}">
    <div class="cta-inner">
      {f'<img src="{LOGO_B64}" class="cta-logo-img" alt="First Class">' if LOGO_B64 else '<div class="cta-logo">FIRST CLASS</div>'}
      <h2 class="cta-title">Соберём поездку <span class="acc">под ключ</span></h2>
      <ul class="cta-list">
        <li>✈️ Авиабилеты из Минска для всей делегации</li>
        <li>🏨 Отель рядом с выставкой</li>
        <li>🚐 Трансферы и визовая поддержка</li>
        <li>💼 Документы для бухгалтерии</li>
      </ul>
      <div class="cta-phone">+375 44 772-52-66</div>
      <div class="cta-handle">{HANDLE}</div>
    </div>
    {progress_bar(idx, total)}
  </div>'''


slides_data = []
total = 1 + len(EXHIBITIONS) + 1
slides_data.append(hero_slide(total))
for i, ex in enumerate(EXHIBITIONS, start=1):
    slides_data.append(exhibition_slide(*ex, i, total))
slides_data.append(cta_slide(total - 1, total))
slides_html = "\n".join(slides_data)

html = f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<title>FC Carousel — Выставки осени 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#222;display:flex;flex-wrap:wrap;gap:24px;padding:40px;justify-content:center;font-family:'Poppins',sans-serif}}
.slide{{width:420px;height:525px;position:relative;overflow:hidden;color:{TEXT};flex-shrink:0}}
.profile{{position:absolute;top:24px;left:28px;display:flex;align-items:center;gap:12px;z-index:5}}
.avatar{{width:38px;height:38px;border-radius:50%;background:{ACCENT};color:{BG_ODD};display:flex;align-items:center;justify-content:center;font-weight:800;font-size:14px}}
.logo-img{{height:34px;width:auto}}
.pname{{font-size:13px;font-weight:700}}
.psub{{font-size:10px;color:{MUTED};letter-spacing:.3px;border-left:1px solid rgba(255,255,255,.2);padding-left:12px}}
.hero-body{{position:absolute;top:50%;transform:translateY(-50%);padding:0 32px}}
.kicker{{color:{ACCENT};font-size:12px;font-weight:700;letter-spacing:3px;margin-bottom:16px}}
.hero h1{{font-size:46px;font-weight:800;line-height:1.05;letter-spacing:-1px}}
.acc{{color:{ACCENT}}}
.hero-sub{{margin-top:18px;font-size:16px;font-style:italic;color:{MUTED};line-height:1.5}}
.ex-body{{position:absolute;top:50%;transform:translateY(-50%);padding:0 32px;width:100%}}
.ex-num{{font-size:60px;font-weight:800;color:{ACCENT};line-height:1}}
.ex-title{{font-family:'Playfair Display',serif;font-size:48px;font-weight:700;margin-top:4px;letter-spacing:-.5px}}
.ex-place{{font-size:16px;font-weight:600;color:{TEXT};margin-top:10px}}
.ex-industry{{display:inline-block;margin-top:14px;padding:6px 16px;border:1px solid {ACCENT};color:{ACCENT};border-radius:30px;font-size:12px;font-weight:600;letter-spacing:.5px;text-transform:uppercase}}
.ex-who{{margin-top:18px;font-size:15px;font-style:italic;color:{MUTED};line-height:1.5;max-width:340px}}
.watermark{{position:absolute;bottom:24px;left:28px;font-size:11px;color:{MUTED};z-index:5}}
.arrow{{position:absolute;bottom:20px;right:28px;font-size:26px;color:{ACCENT};z-index:5}}
.progress{{position:absolute;bottom:0;left:0;right:0;display:flex;gap:3px;padding:0 4px 4px}}
.seg{{flex:1;height:3px;background:rgba(255,255,255,.15);border-radius:2px}}
.seg.on{{background:{ACCENT}}}
.cta-inner{{position:absolute;top:50%;transform:translateY(-50%);padding:0 34px;width:100%}}
.cta-logo{{font-family:'Playfair Display',serif;color:{ACCENT};font-size:22px;letter-spacing:2px;margin-bottom:20px}}
.cta-logo-img{{height:52px;width:auto;margin-bottom:24px}}
.cta-title{{font-size:38px;font-weight:800;line-height:1.1}}
.cta-list{{list-style:none;margin-top:24px}}
.cta-list li{{font-size:15px;color:{TEXT};padding:7px 0;border-bottom:1px solid rgba(255,255,255,.08)}}
.cta-phone{{margin-top:24px;font-size:26px;font-weight:800;color:{ACCENT}}}
.cta-handle{{margin-top:6px;font-size:13px;color:{MUTED}}}
.label{{width:420px;text-align:center;color:#888;font-size:12px;margin-top:-12px}}
</style>
</head>
<body>
{slides_html}
</body>
</html>'''

out = BASE / "2026" / "05" / "carousel-01-vystavki-osen-2026.html"
out.write_text(html, encoding="utf-8")
print(f"OK: {out} ({len(html)} bytes, {total} slides)")
