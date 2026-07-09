#!/usr/bin/env python3
"""Patch FC_ColdEmail_Campaign: switch from HTML to plain-text mode.

Changes:
1. Build Email — append plain-text signature, add `text` field to output.
2. Send Email — emailType: text, body via $json.text.

Strategy: deactivate -> PUT new JSON -> reactivate (n8n requires this).
"""
import os, json, urllib.request, ssl, sys, copy

ctx = ssl.create_default_context()
key = os.environ.get("N8N_API_KEY")
if not key:
    with open(os.path.expanduser("~/.zshrc")) as f:
        for line in f:
            if "N8N_API_KEY" in line and "export" in line:
                key = line.split("=", 1)[1].strip().strip('"').strip("'"); break

WID = "RPVnm6DlyS1AK4JS"
BASE = "https://automation.landingpro.by/api/v1"
H = {"X-N8N-API-KEY": key, "Accept": "application/json", "Content-Type": "application/json"}

def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=H, method=method)
    try:
        return json.loads(urllib.request.urlopen(req, context=ctx, timeout=30).read())
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode("utf-8", errors="replace")[:500]}

# 1. GET current workflow
wf = api("GET", f"/workflows/{WID}")
print("Got:", wf.get("name"), "active=", wf.get("active"))

orig = copy.deepcopy(wf)
backup = f"/Users/admin/Desktop/FirstClass_Automation/scripts/backup_RPVnm6DlyS1AK4JS_{__import__('time').strftime('%Y%m%d_%H%M%S')}.json"
with open(backup, "w") as f:
    json.dump(orig, f, indent=2, ensure_ascii=False)
print(f"Backup saved: {backup}")

# 2. Find Build Email and Send Email nodes
build_node = None
send_node = None
for n in wf["nodes"]:
    if n["name"] == "Build Email":
        build_node = n
    elif n["name"] == "Send Email":
        send_node = n
assert build_node and send_node, "Build Email / Send Email node missing"

# 3. Patch Build Email JS — append signature, return text
SIGNATURE = "\n--\nНадежда Кузнецова\nFirst Class\n+375 44 772-52-66\nhttps://fclass.by"

old_code = build_node["parameters"]["jsCode"]
# Find return statement and inject text field
RETURN_OLD = """// Minimal HTML - just line breaks, no heavy markup
var html = wrapBranded(body);

return [{json: {
  to: item.email,
  subject: subject,
  html: html,
  company: item.company,
  template: template,
  eid: eid
}}];"""
RETURN_NEW = """// Plain-text mode (v2): no HTML wrapping for better deliverability
var signature = "\\n--\\nНадежда Кузнецова\\nFirst Class\\n+375 44 772-52-66\\nhttps://fclass.by";
var text = body + signature;

// Keep html for legacy fallback but Send Email uses text
var html = wrapBranded(body);

return [{json: {
  to: item.email,
  subject: subject,
  text: text,
  html: html,
  company: item.company,
  template: template,
  eid: eid
}}];"""

if RETURN_OLD not in old_code:
    print("FATAL: expected return block not found in Build Email jsCode")
    sys.exit(1)

new_code = old_code.replace(RETURN_OLD, RETURN_NEW)
build_node["parameters"]["jsCode"] = new_code
print("Build Email: jsCode patched (+text field, +signature)")

# 4. Patch Send Email — emailType=text, body via $json.text
send_params = send_node["parameters"]
print("Send Email BEFORE:", {k: send_params.get(k) for k in ("emailType", "text", "html")})
send_params["emailType"] = "text"
send_params["text"] = "={{ $json.text }}"
# remove html if present (n8n keeps it harmless but cleaner without)
if "html" in send_params:
    send_params.pop("html")
print("Send Email AFTER:", {k: send_params.get(k) for k in ("emailType", "text", "html")})

# 5. PUT — n8n requires specific fields only on update
# Strip read-only fields
PUT_FIELDS = ("name", "nodes", "connections", "settings", "staticData")
put_body = {k: wf[k] for k in PUT_FIELDS if k in wf}

# 5a. Deactivate first
print("\nDeactivating...")
deact = api("POST", f"/workflows/{WID}/deactivate")
print("deactivate ->", "OK" if not deact.get("_error") else deact)

# 5b. PUT
print("PUT updated workflow...")
upd = api("PUT", f"/workflows/{WID}", put_body)
if upd.get("_error"):
    print("PUT FAILED:", upd)
    sys.exit(1)
print("PUT OK ->", upd.get("name"))

# 5c. Activate
print("Activating...")
act = api("POST", f"/workflows/{WID}/activate")
print("activate ->", "OK" if not act.get("_error") else act)

# 6. Verify
print("\n--- Verifying ---")
after = api("GET", f"/workflows/{WID}")
for n in after["nodes"]:
    if n["name"] == "Send Email":
        p = n["parameters"]
        print("Send Email NOW:", {k: p.get(k) for k in ("emailType", "text")})
    elif n["name"] == "Build Email":
        c = n["parameters"]["jsCode"]
        has_text = '"text": "" \n' in c or "text: text" in c
        has_sig = "Надежда Кузнецова" in c and "+375 44 772-52-66" in c
        print(f"Build Email: text field={has_text}  signature={has_sig}")
print("active:", after.get("active"))
print("\nDONE")
