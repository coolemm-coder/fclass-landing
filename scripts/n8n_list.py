#!/usr/bin/env python3
"""List n8n workflows on emikss.host, search for cold-email related."""
import os, json, urllib.request, ssl
ctx = ssl.create_default_context()

key = os.environ.get("N8N_API_KEY")
if not key:
    # Try ~/.zshrc
    home = os.path.expanduser("~/.zshrc")
    try:
        with open(home) as f:
            for line in f:
                if "N8N_API_KEY" in line and "export" in line:
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val and not val.startswith("#"):
                        key = val
                        break
    except Exception:
        pass
if not key:
    print("ERR: N8N_API_KEY not in env, not in ~/.zshrc"); raise SystemExit(1)

req = urllib.request.Request(
    "https://emikss.host/api/v1/workflows?limit=200",
    headers={"X-N8N-API-KEY": key, "Accept": "application/json"}
)
data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=15).read())
items = data.get("data", data) if isinstance(data, dict) else data
print(f"Workflows total: {len(items)}\n")
keywords = ["cold", "email", "outreach", "рассылк", "fclass", "marketing", "lead", "pdf", "blog"]
for w in items:
    name = w.get("name", "")
    active = "🟢" if w.get("active") else "⚫"
    wid = w.get("id", "?")
    low = name.lower()
    if any(k in low for k in keywords):
        print(f"  {active}  {wid}  {name}")
print("\n--- all (incl. not-matching) ---")
for w in items:
    name = w.get("name", "")
    active = "🟢" if w.get("active") else "⚫"
    wid = w.get("id", "?")
    print(f"  {active}  {wid}  {name}")
