#!/usr/bin/env python3
"""Patch FC_ManualSend: switch from HTML to plain-text mode.
ManualSend takes {body:{to,subject,text}} via webhook. We just need to:
- Build Email: append signature, return text instead of wrapping
- Send Email: emailType=text, text=$json.text
"""
import os, json, urllib.request, ssl, copy, time, sys
ctx = ssl.create_default_context()
key = os.environ.get("N8N_API_KEY")
if not key:
    with open(os.path.expanduser("~/.zshrc")) as f:
        for line in f:
            if "N8N_API_KEY" in line and "export" in line:
                key = line.split("=", 1)[1].strip().strip('"').strip("'"); break

WID = "H8YOY2gf3rZANXFl"
BASE = "https://automation.landingpro.by/api/v1"
H = {"X-N8N-API-KEY": key, "Accept": "application/json", "Content-Type": "application/json"}

def api(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, headers=H, method=method)
    try:
        return json.loads(urllib.request.urlopen(req, context=ctx, timeout=30).read())
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode("utf-8", errors="replace")[:500]}

wf = api("GET", f"/workflows/{WID}")
print("Got:", wf.get("name"), "active=", wf.get("active"))
backup = f"/Users/admin/Desktop/FirstClass_Automation/scripts/backup_{WID}_{time.strftime('%Y%m%d_%H%M%S')}.json"
with open(backup, "w") as f:
    json.dump(wf, f, indent=2, ensure_ascii=False)
print(f"Backup: {backup}")

build = None; send = None
for n in wf["nodes"]:
    if n["name"] == "Build Email": build = n
    elif n["name"] == "Send Email": send = n

OLD_TAIL = "var b = $input.first().json.body || {};var to = b.to || '';var subject = b.subject || '';var text = b.text || '';if (!to || !subject || !text) return [{json:{error:'Missing to/subject/text'}}];var html = wrapBranded(text);return [{json: {to: to, subject: subject, html: html}}];"

# Build a more robust matcher: the JS may have whitespace differences
code = build["parameters"]["jsCode"]
# Locate the simple input/return part — last 400 chars
idx = code.find("var b = $input.first().json.body")
if idx == -1:
    print("FATAL: handler start not found")
    sys.exit(1)
handler_old = code[idx:]
print("Handler OLD length:", len(handler_old))

handler_new = (
    "var b = $input.first().json.body || {};\n"
    "var to = b.to || '';\n"
    "var subject = b.subject || '';\n"
    "var text = b.text || '';\n"
    "if (!to || !subject || !text) return [{json:{error:'Missing to/subject/text'}}];\n"
    "// Plain-text mode (v2): append signature, no HTML wrap\n"
    "var signature = \"\\n--\\nНадежда Кузнецова\\nFirst Class\\n+375 44 772-52-66\\nhttps://fclass.by\";\n"
    "var plainText = text + signature;\n"
    "return [{json: {to: to, subject: subject, text: plainText}}];"
)
new_code = code[:idx] + handler_new
build["parameters"]["jsCode"] = new_code
print("Build Email handler replaced (text mode + signature)")

# Patch Send Email
sp = send["parameters"]
print("Send Email BEFORE:", {k: sp.get(k) for k in ("emailType", "text", "html")})
sp["emailType"] = "text"
sp["text"] = "={{ $json.text }}"
if "html" in sp:
    sp.pop("html")
print("Send Email AFTER:", {k: sp.get(k) for k in ("emailType", "text", "html")})

# Deactivate -> PUT -> Activate
PUT_FIELDS = ("name", "nodes", "connections", "settings", "staticData")
put_body = {k: wf[k] for k in PUT_FIELDS if k in wf}

print("\nDeactivating..."); r = api("POST", f"/workflows/{WID}/deactivate"); print("->", "OK" if not r.get("_error") else r)
print("PUT..."); r = api("PUT", f"/workflows/{WID}", put_body)
if r.get("_error"):
    print("FAIL:", r); sys.exit(1)
print("-> OK")
print("Activating..."); r = api("POST", f"/workflows/{WID}/activate"); print("->", "OK" if not r.get("_error") else r)

# Verify
after = api("GET", f"/workflows/{WID}")
for n in after["nodes"]:
    if n["name"] == "Send Email":
        p = n["parameters"]
        print("Send Email NOW:", {k: p.get(k) for k in ("emailType", "text")})
    elif n["name"] == "Build Email":
        c = n["parameters"]["jsCode"]
        print("Build Email signature present:", "Надежда Кузнецова" in c, "plain mode:", "return [{json: {to: to, subject: subject, text: plainText}}]" in c)
print("active:", after.get("active"))
print("DONE")
