import sys, re
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    print("===", f, "===")
    checks = {
        'webhook fc-lead': s.count('emikss.host/webhook/fc-lead'),
        'data-lead-form': s.count('data-lead-form'),
        'reachGoal LEAD': s.count("reachGoal','LEAD'"),
        'cta-thanks': s.count('cta-thanks'),
        'source hidden': len(re.findall(r'name="source"', s)),
        'tg fclassmsk_bot': s.count('fclassmsk_bot'),
        'marketing@fclass.by': s.count('marketing@fclass.by'),
        'info@ (must be 0)': s.count('info@fclass.by'),
        'mobnav.js': s.count('/assets/mobnav.js'),
        'onerror (must be 0)': s.count('onerror'),
        'footer-logo-text (must be 0)': s.count('footer-logo-text'),
        'footer-brand (should be 0)': s.count('footer-brand'),
        'footer-social': s.count('footer-social'),
        'WhatsApp wa.me': s.count('wa.me/375447725266'),
        'tg firstclassby (footer)': s.count('t.me/firstclassby'),
        'JSON-LD blocks': s.count('application/ld+json'),
        'FAQPage': s.count('FAQPage'),
        'BreadcrumbList': s.count('BreadcrumbList'),
        'BlogPosting': s.count('BlogPosting'),
        'canonical': s.count('rel="canonical"'),
        'og:type article': s.count('og:type" content="article"'),
        'robots index': s.count('index, follow'),
        'article-img': s.count('class="article-img"'),
        'tickets/minsk-baku/': s.count('/tickets/minsk-baku/'),
        'tickets/minsk-erevan/': s.count('/tickets/minsk-erevan/'),
        'komandirovki/': s.count('/komandirovki/'),
        'aviabilety-dlya-yurlic': s.count('/tickets/aviabilety-dlya-yurlic/'),
        'aggregators (must be 0)': sum(s.lower().count(x) for x in ['skyscanner','aviasales','kayak','momondo','google flights']),
    }
    for k, v in checks.items():
        print("  %-30s %s" % (k, v))
    for tag in ['div', 'article', 'form', 'footer', 'section']:
        o = len(re.findall(r'<%s[ >]' % tag, s))
        c = len(re.findall(r'</%s>' % tag, s))
        print("  <%s> open=%d close=%d %s" % (tag, o, c, 'OK' if o == c else 'MISMATCH'))
