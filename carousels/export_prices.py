import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
BASE = Path(__file__).parent
HTML = BASE / "2026" / "05" / "cards-from-prices.html"
OUT = BASE / "2026" / "05" / "png"
OUT.mkdir(exist_ok=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(device_scale_factor=2.5714)
        await pg.goto(f"file://{HTML}")
        await pg.wait_for_timeout(1500)
        cards = await pg.query_selector_all(".card")
        for i, c in enumerate(cards, 1):
            await c.screenshot(path=str(OUT / f"price-card-{i:02d}.png"))
        await b.close()
    print(f"Exported {len(cards)} cards")
asyncio.run(main())
