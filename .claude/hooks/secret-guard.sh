#!/bin/bash
# =============================================================================
# Secret Guard Hook — PreToolUse (Write|Edit)
# Blocks writes to sensitive files and detects API keys in content
# Adapted for FirstClass_Automation + FC_LeadRouter projects
# =============================================================================

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('tool_input', {}).get('file_path', ''))
except:
    print('')
" 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
    exit 0
fi

BASENAME=$(basename "$FILE_PATH")

# Block patterns for sensitive files
BLOCKED_PATTERNS=(
    "\.env$"
    "\.env\."
    "\.pem$"
    "\.key$"
    "\.p12$"
    "credentials"
    "secrets?\."
    "\.secret"
    "id_rsa"
    "id_ed25519"
    "\.npmrc$"
    "\.pypirc$"
    "auth.*\.json$"
    "service.account.*\.json$"
    "token.*\.json$"
    "\.zshrc$"
    "\.bashrc$"
)

for pattern in "${BLOCKED_PATTERNS[@]}"; do
    if echo "$BASENAME" | grep -qiE "$pattern"; then
        echo "BLOCKED: Cannot write to sensitive file '$BASENAME'. Secrets must be managed manually by the user." >&2
        exit 2
    fi
done

# Check file content for API keys / tokens
echo "$INPUT" | python3 -c "
import sys, json, re
try:
    data = json.load(sys.stdin)
    content = data.get('tool_input', {}).get('content', '')
    if not content:
        content = data.get('tool_input', {}).get('new_string', '')
    if not content:
        sys.exit(0)
    patterns = [
        (r'(?:api[_-]?key|apikey)\s*[=:]\s*[\"'\'']\S{20,}', 'API key'),
        (r'(?:secret|password|passwd|pwd)\s*[=:]\s*[\"'\'']\S{8,}', 'password/secret'),
        (r'-----BEGIN (?:RSA |EC )?PRIVATE KEY-----', 'private key'),
        (r'sk-[a-zA-Z0-9]{20,}', 'OpenAI/Anthropic key'),
        (r'ghp_[a-zA-Z0-9]{36}', 'GitHub token'),
        (r'gho_[a-zA-Z0-9]{36}', 'GitHub OAuth token'),
        (r'bot\d{8,}:[A-Za-z0-9_-]{35}', 'Telegram bot token'),
        (r'xox[bpoas]-[a-zA-Z0-9-]+', 'Slack token'),
        (r'N8N_API_KEY\s*=\s*\S+', 'n8n API key'),
    ]
    for p, name in patterns:
        if re.search(p, content, re.IGNORECASE):
            print(f'BLOCKED: Content contains what looks like a {name}. Do NOT hardcode secrets — use .env or n8n credentials.', file=sys.stderr)
            sys.exit(2)
except Exception:
    pass
sys.exit(0)
" 2>&1
exit $?
