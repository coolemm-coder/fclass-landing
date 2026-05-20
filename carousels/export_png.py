import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE = Path(__file__).parent
HTML = BASE / "2026" / "05" / "carousel-01-vystavki-osen-2026.html"
OUT = BASE / "2026" / "05" / "png"
OUT.mkdir(exist_ok=True)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(device_scale_factor=2.5714)
        await page.goto(f"file://{HTML}")
        await page.wait_for_timeout(1500)
        slides = await page.query_selector_all(".slide")
        print(f"Found {len(slides)} slides")
        for i, slide in enumerate(slides, 1):
            await slide.screenshot(path=str(OUT / f"slide-{i:02d}.png"))
        await browser.close()
    print(f"Exported {len(slides)} PNGs to {OUT}")

asyncio.run(main())
