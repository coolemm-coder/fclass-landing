#!/bin/bash
set -u
echo "=== Latest commits ==="
/usr/bin/python3 /Users/admin/Desktop/FirstClass_Automation/scripts/check_runs.py
echo
echo "=== Live HTTP checks ==="
URLS=(
  "https://fclass.by/"
  "https://fclass.by/komandirovki/"
  "https://fclass.by/tickets/aviabilety-dlya-yurlic/"
  "https://fclass.by/resources/dogovor-template/"
  "https://fclass.by/resources/calculator/"
  "https://fclass.by/cases/"
  "https://fclass.by/sitemap.xml"
  "https://fclass.by/blog/korporativnye-aviabilety-minsk.html"
  "https://landingpro.by/"
)
for u in "${URLS[@]}"; do
  code=$(curl -sI "$u" -o /dev/null -w "%{http_code}")
  echo "  $code  $u"
done
echo
echo "=== Forbidden terms check ==="
for u in "https://fclass.by/komandirovki/" "https://fclass.by/tickets/aviabilety-dlya-yurlic/"; do
  body=$(curl -s "$u")
  bad=$(echo "$body" | grep -oE "15-25%|корпоративный договор|турагентство|Окупаемость 1-2|НДС автоматически" | sort -u)
  if [ -z "$bad" ]; then
    echo "  CLEAN  $u"
  else
    echo "  DIRTY  $u  ->  $bad"
  fi
done
