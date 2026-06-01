#!/usr/bin/env python3
"""
FC email parser — собирает контактные email компаний по их сайтам.
Вход: CSV с колонками name,email,website,... (по умолчанию data/all_contacts.csv).
Логика: для строк с website и без email — тянет homepage + типовые контакт-страницы,
извлекает email регуляркой, фильтрует мусор/чужие домены, выбирает лучший (info@/sales@/etc),
пишет результат в новый CSV + лог. Переиспользуемо для любого списка сайтов.

Запуск:
  python3 scripts/email_parser.py                      # all_contacts.csv, только site-no-email
  python3 scripts/email_parser.py --limit 50           # первые 50 целей (тест)
  python3 scripts/email_parser.py --in path.csv --out path.enriched.csv
"""
import csv, re, sys, time, argparse, urllib.request, urllib.error
from urllib.parse import urlparse, urljoin

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
CONTACT_PATHS = ['', 'contacts/', 'contacts', 'kontakty/', 'kontakty', 'contact/', 'contact',
                 'about/', 'about', 'o-kompanii/', 'company/']
# мусорные/не-целевые адреса
BAD_SUBSTR = ['example.', 'sentry.', 'wixpress.', '.png', '.jpg', '.jpeg', '.gif', '.webp',
              '@sentry', 'cloudflare', 'godaddy', 'domain', 'youremail', 'email@', 'name@',
              'u00', '%', 'core-js', 'react', 'schema.org']
PERSONAL_DOMAINS = ['gmail.com', 'mail.ru', 'yandex.ru', 'yandex.by', 'tut.by', 'list.ru',
                    'inbox.ru', 'bk.ru', 'rambler.ru', 'icloud.com', 'outlook.com', 'hotmail.com']
PREFIX_RANK = ['info', 'office', 'sales', 'mail', 'hello', 'contact', 'company', 'reception',
               'secretary', 'hr', 'zakaz', 'market']
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/124.0 Safari/537.36'}


def root_domain(website):
    w = website.strip()
    if not w.startswith('http'):
        w = 'https://' + w
    netloc = urlparse(w).netloc.lower()
    return netloc[4:] if netloc.startswith('www.') else netloc, w


def fetch(url, timeout=12):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            ct = r.headers.get('Content-Type', '')
            if 'html' not in ct and 'text' not in ct:
                return ''
            return r.read(600000).decode('utf-8', errors='ignore')
    except Exception:
        return ''


def clean_candidates(text, domain):
    found = set()
    for m in EMAIL_RE.findall(text):
        e = m.strip().lower().rstrip('.')
        if any(b in e for b in BAD_SUBSTR):
            continue
        if len(e) > 60 or e.count('@') != 1:
            continue
        found.add(e)
    return found


def pick_best(emails, domain):
    if not emails:
        return ''
    # 1) на домене компании — приоритет
    same = [e for e in emails if e.split('@')[1] == domain or e.split('@')[1].endswith('.' + domain)]
    # 2) иначе — только личные провайдеры (часто реальный контакт малого бизнеса РБ);
    #    чужие сервис-домены (catalog.app и пр.) НЕ берём — это виджеты/ложные плюсы
    personal = [e for e in emails if e.split('@')[1] in PERSONAL_DOMAINS]
    pool = same if same else personal
    if not pool:
        return ''
    # 2) ранжируем по префиксу
    def score(e):
        p = e.split('@')[0]
        for i, pref in enumerate(PREFIX_RANK):
            if p == pref or p.startswith(pref):
                return i
        return len(PREFIX_RANK) + 1
    pool.sort(key=score)
    return pool[0]


def find_email_for(website):
    domain, base = root_domain(website)
    if not domain:
        return '', ''
    all_found = set()
    for path in CONTACT_PATHS:
        url = urljoin(base if base.endswith('/') else base + '/', path)
        html = fetch(url)
        if html:
            all_found |= clean_candidates(html, domain)
        if path in ('contacts/', 'kontakty/') and all_found:
            break  # нашли на контактах — хватит
        time.sleep(0.3)
    best = pick_best(all_found, domain)
    return best, ';'.join(sorted(all_found)[:5])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='inp', default='/Users/admin/Desktop/FirstClass_Automation/data/all_contacts.csv')
    ap.add_argument('--out', dest='out', default='/Users/admin/Desktop/FirstClass_Automation/data/all_contacts.enriched.csv')
    ap.add_argument('--limit', type=int, default=0)
    args = ap.parse_args()

    rows = list(csv.DictReader(open(args.inp, encoding='utf-8', errors='ignore')))
    fields = list(rows[0].keys())
    if 'email_found' not in fields:
        fields += ['email_found', 'email_candidates']

    targets = [r for r in rows if (r.get('website') or '').strip() and not (r.get('email') or '').strip()]
    if args.limit:
        targets = targets[:args.limit]
    print(f"целей (site-no-email): {len(targets)}")

    found = 0
    for i, r in enumerate(targets, 1):
        best, cands = find_email_for(r['website'])
        r['email_found'] = best
        r['email_candidates'] = cands
        if best:
            r['email'] = best  # заполняем основную колонку
            found += 1
        print(f"  [{i}/{len(targets)}] {(r.get('name') or '')[:28]:28} {r['website'][:34]:34} -> {best or '—'}")

    with open(args.out, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    print(f"\nНайдено email: {found}/{len(targets)} | сохранено: {args.out}")


if __name__ == '__main__':
    main()
