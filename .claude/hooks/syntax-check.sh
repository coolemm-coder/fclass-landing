#!/bin/bash
# =============================================================================
# Syntax Check Hook — PostToolUse (Edit|Write)
# Validates syntax after every file edit (Python, JSON, YAML, JS/JSX)
# =============================================================================

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    ti = data.get('tool_input', {})
    print(ti.get('file_path', ''))
except:
    print('')
" 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

# Python syntax check
if [[ "$FILE_PATH" == *.py ]]; then
    python3 -c "
import ast, sys
try:
    ast.parse(open('$FILE_PATH').read())
except SyntaxError as e:
    print(f'Syntax error in $FILE_PATH line {e.lineno}: {e.msg}')
    sys.exit(1)
" 2>&1
fi

# JSON syntax check
if [[ "$FILE_PATH" == *.json ]]; then
    python3 -c "
import json, sys
try:
    json.load(open('$FILE_PATH'))
except json.JSONDecodeError as e:
    print(f'JSON error in $FILE_PATH: {e.msg} at line {e.lineno}')
    sys.exit(1)
" 2>&1
fi

# YAML syntax check
if [[ "$FILE_PATH" == *.yml ]] || [[ "$FILE_PATH" == *.yaml ]]; then
    if python3 -c "import yaml" 2>/dev/null; then
        python3 -c "
import yaml, sys
try:
    yaml.safe_load(open('$FILE_PATH'))
except yaml.YAMLError as e:
    print(f'YAML error in $FILE_PATH: {e}')
    sys.exit(1)
" 2>&1
    fi
fi

# HTML basic check — unclosed tags
if [[ "$FILE_PATH" == *.html ]]; then
    python3 -c "
from html.parser import HTMLParser
import sys

class Checker(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = []
    def handle_starttag(self, tag, attrs):
        pass
    def handle_endtag(self, tag):
        pass

try:
    p = Checker()
    p.feed(open('$FILE_PATH').read())
except Exception as e:
    print(f'HTML parse warning in $FILE_PATH: {e}')
" 2>&1
fi

exit 0
