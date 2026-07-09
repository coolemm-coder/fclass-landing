#!/usr/bin/env python3
"""Get specific workflow detail."""
import os, json, urllib.request, ssl, sys
ctx = ssl.create_default_context()

key = os.environ.get("N8N_API_KEY")
if not key:
    with open(os.path.expanduser("~/.zshrc")) as f:
        for line in f:
            if "N8N_API_KEY" in line and "export" in line:
                key = line.split("=", 1)[1].strip().strip('"').strip("'"); break

wid = sys.argv[1]
req = urllib.request.Request(
    f"https://automation.landingpro.by/api/v1/workflows/{wid}",
    headers={"X-N8N-API-KEY": key, "Accept": "application/json"}
)
data = json.loads(urllib.request.urlopen(req, context=ctx, timeout=15).read())
print("Name:", data.get("name"))
print("Active:", data.get("active"))
print("Nodes:")
for n in data.get("nodes", []):
    typ = n.get("type", "")
    name = n.get("name", "")
    pos = n.get("position", [0, 0])
    print(f"  - {name}  ({typ})  @ {pos}")
# dump full to file for analysis
out = f"/tmp/{wid}.json"
with open(out, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print(f"\nFull dump: {out}")
