#!/usr/bin/env python3
"""
cci.by Belarusian Exporters Parser
Парсит каталог "Белорусские экспортёры" — 2774 компании с email.
Все экспортёры = потенциальные клиенты для корп.тревела.
"""

import csv
import re
import sys
import time
import json
from pathlib import Path
from urllib.parse import quote
from playwright.sync_api import sync_playwright

BASE_URL = "https://www.cci.by"
CATALOG_URL = (
    "https://www.cci.by/belorusskie-eksportery/"
    "?search=Y&q="
    "&REGION%5B0%5D=%D0%91%D1%80%D0%B5%D1%81%D1%82%D1%81%D0%BA%D0%B0%D1%8F"
    "&REGION%5B1%5D=%D0%92%D0%B8%D1%82%D0%B5%D0%B1%D1%81%D0%BA%D0%B0%D1%8F"
    "&REGION%5B2%5D=%D0%93%D0%BE%D0%BC%D0%B5%D0%BB%D1%8C%D1%81%D0%BA%D0%B0%D1%8F"
    "&REGION%5B3%5D=%D0%93%D1%80%D0%BE%D0%B4%D0%BD%D0%B5%D0%BD%D1%81%D0%BA%D0%B0%D1%8F"
    "&REGION%5B4%5D=%D0%9C%D0%B8%D0%BD%D1%81%D0%BA%D0%B0%D1%8F"
    "&REGION%5B5%5D=%D0%9C%D0%BE%D0%B3%D0%B8%D0%BB%D1%91%D0%B2%D1%81%D0%BA%D0%B0%D1%8F"
    "&set_filter=%D0%9F%D0%BE%D0%BA%D0%B0%D0%B7%D0%B0%D1%82%D1%8C"
    "&PAGEN_2={page}"
)

OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_CSV = OUTPUT_DIR / "cci_exporters.csv"
OUTPUT_JSON = OUTPUT_DIR / "cci_exporters.json"


def parse_page(page, page_num: int) -> list[dict]:
    """Parse one page of exporter catalog (20 items per page)."""
    url = CATALOG_URL.format(page=page_num)
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception:
        page.goto(url, timeout=30000)
    time.sleep(1)

    companies = page.evaluate("""
        () => {
            const results = [];
            // Each company is in a card/block with name and details
            const items = document.querySelectorAll('.catalog-export-item, .export-item, .company-card');

            if (items.length > 0) {
                items.forEach(item => {
                    const name = item.querySelector('h3, h4, .name, a')?.textContent?.trim() || '';
                    const text = item.innerText;
                    const html = item.innerHTML;
                    const emailMatch = html.match(/[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}/g);
                    const phoneMatch = text.match(/\\+375[\\d\\s\\-()]+/g);
                    const siteMatch = html.match(/https?:\\/\\/[^\\s"'<>]+/g);

                    results.push({
                        name: name,
                        email: emailMatch ? emailMatch[0] : '',
                        phone: phoneMatch ? phoneMatch[0].trim() : '',
                        website: siteMatch ? siteMatch.filter(s => !s.includes('cci.by'))[0] || '' : ''
                    });
                });
            } else {
                // Fallback: parse from page text
                const text = document.body.innerText;
                const html = document.body.innerHTML;

                // Try to find company blocks by looking at the structure
                const allEmails = html.match(/[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}/g) || [];
                const uniqueEmails = [...new Set(allEmails)].filter(e => !e.includes('cci.by'));

                // Find company names - they appear as links or bold text before email
                const nameBlocks = text.split('\\n').filter(l => l.trim().length > 10 && !l.includes('@') && !l.includes('+375'));

                uniqueEmails.forEach((email, i) => {
                    results.push({
                        name: '',
                        email: email,
                        phone: '',
                        website: ''
                    });
                });
            }

            return results;
        }
    """)

    return companies


def parse_page_v3(page, page_num: int) -> list[dict]:
    """Parse accordion panels: .item.panel.panel-default.timing."""
    url = CATALOG_URL.format(page=page_num)
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
    except Exception:
        page.goto(url, timeout=30000)
    time.sleep(0.5)

    js_code = (
        "() => {"
        "  const results = [];"
        "  const panels = document.querySelectorAll('.item.panel.panel-default.timing');"
        "  panels.forEach(panel => {"
        "    const name = panel.querySelector('.panel-title')?.textContent?.trim() || '';"
        "    const body = panel.querySelector('.panel-collapse');"
        "    if (!body) { results.push({name:name,email:'',phone:'',website:'',address:'',description:''}); return; }"
        "    const html = body.innerHTML;"
        "    const mailtoMatch = html.match(/mailto:([^\"]+)/);"
        "    const email = mailtoMatch ? mailtoMatch[1] : '';"
        "    const siteLink = body.querySelector('a[target=\"_blank\"]');"
        "    const website = siteLink ? siteLink.textContent.trim() : '';"
        "    const divs = body.querySelectorAll('div');"
        "    let phone = '', address = '', description = '';"
        "    divs.forEach(d => {"
        "      const t = d.textContent.trim();"
        "      const b = d.querySelector('b');"
        "      if (!b) return;"
        "      const label = b.textContent.trim();"
        "      const val = t.replace(label, '').trim();"
        "      if (label.indexOf('\\u0410\\u0434\\u0440\\u0435\\u0441') >= 0) address = val;"
        "      if (label.indexOf('\\u0422\\u0435\\u043b\\u0435\\u0444\\u043e\\u043d') >= 0) phone = val;"
        "      if (label.indexOf('\\u041e\\u043f\\u0438\\u0441\\u0430\\u043d\\u0438\\u0435') >= 0) description = val;"
        "    });"
        "    results.push({name:name,email:email,phone:phone,website:website,address:address,description:description});"
        "  });"
        "  return results;"
        "}"
    )
    data = page.evaluate(js_code)

    return data


def main():
    print("=" * 60)
    print("Parsing cci.by Belarusian Exporters catalog...")
    print("=" * 60)
    sys.stdout.flush()

    all_companies = []
    seen_emails = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        )
        page = context.new_page()

        # 2774 companies, 20 per page = 139 pages
        total_pages = 139
        for page_num in range(1, total_pages + 1):
            companies = parse_page_v3(page, page_num)

            new_count = 0
            for c in companies:
                email = c.get("email", "")
                if email and email not in seen_emails:
                    seen_emails.add(email)
                    all_companies.append(c)
                    new_count += 1
                elif not email and c.get("name"):
                    all_companies.append(c)
                    new_count += 1

            print(f"  Page {page_num}/{total_pages}: {new_count} new (total: {len(all_companies)})")
            sys.stdout.flush()

            time.sleep(0.5)

        browser.close()

    # Save
    print(f"\n{'=' * 60}")
    print("Saving results...")

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(all_companies, f, ensure_ascii=False, indent=2)

    fields = ["name", "email", "phone", "website", "address", "description"]
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(all_companies)

    with_email = sum(1 for c in all_companies if c.get("email"))
    print(f"  CSV: {OUTPUT_CSV}")
    print(f"  JSON: {OUTPUT_JSON}")
    print(f"\nDONE! {len(all_companies)} companies")
    print(f"  With email: {with_email}")
    print(f"{'=' * 60}")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
