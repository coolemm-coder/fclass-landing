#!/usr/bin/env python3
"""
Park.by HTP Residents Parser v2 (curl + playwright hybrid)
Step 1: curl to collect all company URLs (fast, via pagination)
Step 2: playwright to parse each company detail page (needs JS)

Output: CSV + JSON with contacts of all 1060+ HTP residents
"""

import csv
import re
import sys
import time
import json
import subprocess
from pathlib import Path
from urllib.parse import quote

BASE_URL = "https://park.by"
OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / "park_by_residents.csv"
OUTPUT_JSON = OUTPUT_DIR / "park_by_residents.json"

LETTERS = list("АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЭЮЯ") + list("123456789") + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")


def curl_get(url: str) -> str:
    """Fetch URL content via curl."""
    result = subprocess.run(
        ["curl", "-s", "-H", "User-Agent: Mozilla/5.0", url],
        capture_output=True, text=True, timeout=30
    )
    return result.stdout


def collect_all_urls() -> list[dict]:
    """Collect all company URLs using curl pagination."""
    print("=" * 60)
    print("STEP 1: Collecting company URLs (curl + pagination)...")
    print("=" * 60)
    sys.stdout.flush()

    all_links = []
    seen = set()

    for letter in LETTERS:
        encoded = quote(letter)
        page_num = 1
        letter_count = 0

        while True:
            url = f"{BASE_URL}/residents/?first={encoded}&PAGEN_1={page_num}"
            html = curl_get(url)

            # Extract company links
            matches = re.findall(r'href="/residents/([^"]+)/"', html)
            # Filter out non-company links
            company_slugs = [m for m in matches if m not in ("", "search") and not m.startswith("?")]

            new_count = 0
            for slug in company_slugs:
                if slug not in seen:
                    seen.add(slug)
                    # Try to extract name from the HTML context
                    name_match = re.search(
                        rf'href="/residents/{re.escape(slug)}/"[^>]*><b>([^<]+)</b>',
                        html
                    )
                    name = name_match.group(1) if name_match else slug
                    all_links.append({"url": f"/residents/{slug}/", "name": name})
                    new_count += 1
                    letter_count += 1

            # Check if there's a next page
            next_page = f"PAGEN_1={page_num + 1}"
            if next_page in html and new_count > 0:
                page_num += 1
                time.sleep(0.3)  # Be polite
            else:
                break

        if letter_count > 0:
            print(f"  Letter '{letter}': {letter_count} companies (total: {len(all_links)})")
            sys.stdout.flush()

    print(f"\nTotal unique companies: {len(all_links)}")
    sys.stdout.flush()
    return all_links


def parse_company_pages(links: list[dict]) -> list[dict]:
    """Parse company detail pages using playwright."""
    from playwright.sync_api import sync_playwright

    print("\n" + "=" * 60)
    print(f"STEP 2: Parsing {len(links)} company detail pages...")
    print("=" * 60)
    sys.stdout.flush()

    all_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()

        for i, link in enumerate(links):
            full_url = f"{BASE_URL}{link['url']}"
            name = link["name"]

            try:
                page.goto(full_url, wait_until="domcontentloaded", timeout=15000)
                time.sleep(0.5)

                data = page.evaluate("""
                    () => {
                        const text = document.body.innerText;
                        const html = document.body.innerHTML;

                        const getField = (label) => {
                            const regex = new RegExp(label + ':\\\\s*(.+?)\\\\n', 'i');
                            const match = text.match(regex);
                            return match ? match[1].trim() : '';
                        };

                        const emailMatch = html.match(/[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}/g);
                        const emails = emailMatch ? [...new Set(emailMatch)].filter(e =>
                            !e.includes('bitrix') && !e.includes('park.by')
                        ) : [];

                        const siteMatch = html.match(/https?:\\/\\/[^\\s"'<>]+/g);
                        const sites = siteMatch ? [...new Set(siteMatch)].filter(s =>
                            !s.includes('park.by') && !s.includes('bitrix') &&
                            !s.includes('google') && !s.includes('facebook') &&
                            !s.includes('instagram') && !s.includes('linkedin') &&
                            !s.includes('telegram') && !s.includes('font') &&
                            !s.includes('stackpath') && !s.includes('president') &&
                            !s.includes('government') && !s.includes('cdn') &&
                            !s.includes('cookie')
                        ) : [];

                        return {
                            unp: getField('УНП'),
                            employees: getField('Количество сотрудников'),
                            city: getField('Город'),
                            address: getField('Юридический адрес'),
                            email: getField('Адрес электронной почты') || (emails.length > 0 ? emails[0] : ''),
                            website: getField('Веб-сайт') || (sites.length > 0 ? sites[0] : ''),
                            year: getField('Год основания'),
                            activities: getField('Направления деятельности'),
                            industry: getField('Отрасль применения')
                        };
                    }
                """)

                data["name"] = name
                data["url"] = full_url
                all_data.append(data)

                email_status = data.get("email", "")
                status = f"✓ {email_status}" if email_status else "✗"
                print(f"  [{i+1}/{len(links)}] {name[:45]:45s} {status}")
                sys.stdout.flush()

            except Exception as e:
                all_data.append({"name": name, "url": full_url, "error": str(e)})
                print(f"  [{i+1}/{len(links)}] {name[:45]:45s} ERROR: {e}")
                sys.stdout.flush()

            # Polite delay every 20 requests
            if i % 20 == 19:
                time.sleep(2)

        browser.close()

    return all_data


def save_results(companies: list[dict]):
    """Save to CSV and JSON."""
    print("\n" + "=" * 60)
    print("STEP 3: Saving results...")
    print("=" * 60)

    # JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(companies, f, ensure_ascii=False, indent=2)
    print(f"  JSON: {OUTPUT_JSON}")

    # CSV
    fields = ["name", "email", "website", "city", "employees", "unp",
              "address", "year", "industry", "activities", "url"]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(companies)
    print(f"  CSV: {OUTPUT_CSV}")

    # Stats
    with_email = sum(1 for c in companies if c.get("email"))
    with_site = sum(1 for c in companies if c.get("website"))
    print(f"\n{'=' * 60}")
    print(f"DONE! {len(companies)} companies parsed")
    print(f"  With email: {with_email}")
    print(f"  With website: {with_site}")
    print(f"  Without email: {len(companies) - with_email}")
    print(f"{'=' * 60}")
    sys.stdout.flush()


def main():
    links = collect_all_urls()
    companies = parse_company_pages(links)
    save_results(companies)


if __name__ == "__main__":
    main()
