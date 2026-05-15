#!/bin/bash
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'

echo '=== Live HTTP checks (curl GET) ==='
for u in \
  'https://fclass.by/' \
  'https://fclass.by/komandirovki/' \
  'https://fclass.by/tickets/aviabilety-dlya-yurlic/' \
  'https://fclass.by/resources/dogovor-template/' \
  'https://fclass.by/resources/calculator/' \
  'https://fclass.by/cases/' \
  'https://fclass.by/sitemap.xml' \
  'https://fclass.by/blog/korporativnye-aviabilety-minsk.html' \
  'https://landingpro.by/'; do
  code=$(curl -sS -o /dev/null -w '%{http_code}' -A "$UA" --max-time 12 "$u")
  echo "  $code  $u"
done

echo
echo '=== Forbidden terms check ==='
for u in 'https://fclass.by/komandirovki/' 'https://fclass.by/tickets/aviabilety-dlya-yurlic/'; do
  body=$(curl -sS -A "$UA" --max-time 12 "$u")
  bad=$(echo "$body" | grep -oE '15-25%|корпоративный договор|турагентство|Окупаемость 1-2|НДС автоматически')
  if [ -z "$bad" ]; then
    echo "  CLEAN  $u"
  else
    echo "  DIRTY  $u  ->"
    echo "$bad" | sort -u | sed 's/^/      /'
  fi
done
