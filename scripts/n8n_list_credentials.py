#!/usr/bin/env python3
"""List n8n credentials (names + types only — values not exposed by API)."""
import os, json, urllib.request, ssl
ctx = ssl.create_default_context()
key = os.environ.get("N8N_API_KEY")
if not key:
    with open(os.path.expanduser("~/.zshrc")) as f:
        for line in f:
            if "N8N_API_KEY" in line and "export" in line:
                key = line.split("=", 1)[1].strip().strip('"').strip("'"); break

# n8n public REST API doesn't have GET /credentials list endpoint by default.
# But we can inspect workflows for which credentials they use.
req = urllib.request.Request("https://automation.landingpro.by/api/v1/workflows?limit=200",
    headers={"X-N8N-API-KEY": key, "Accept": "application/json"})
data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=15).read())
items = data.get("data", data) if isinstance(data, dict) else data

cred_map = {}  # cred_id -> {name, type, used_in_workflows}
for wf in items:
    wid = wf.get("id"); wname = wf.get("name", "")
    for node in wf.get("nodes", []):
        creds = node.get("credentials", {})
        for ctype, c in creds.items():
            if not isinstance(c, dict): continue
            cid = c.get("id"); cname = c.get("name", "")
            if not cid: continue
            entry = cred_map.setdefault(cid, {"name": cname, "type": ctype, "used_in": set()})
            entry["used_in"].add(wname)

print(f"Discovered {len(cred_map)} credentials referenced in workflows\n")
# Filter for email/smtp/mail
print("=== Email/SMTP credentials ===")
for cid, info in cred_map.items():
    if "smtp" in info["type"].lower() or "mail" in info["type"].lower() or "email" in info["type"].lower():
        print(f"  ID: {cid}")
        print(f"    name: {info['name']}")
        print(f"    type: {info['type']}")
        print(f"    used in {len(info['used_in'])} workflows: {sorted(info['used_in'])[:5]}")
        print()

print("=== All credentials (top 40) ===")
for cid, info in list(cred_map.items())[:40]:
    print(f"  {info['type']:40s} name={info['name'][:30]:30s} ({len(info['used_in'])} wfs)")
