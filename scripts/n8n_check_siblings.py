#!/usr/bin/env python3
"""Check FC_ColdEmail_Scheduler and FC_ManualSend for HTML email nodes."""
import os, json, urllib.request, ssl
ctx = ssl.create_default_context()
key = os.environ.get("N8N_API_KEY")
if not key:
    with open(os.path.expanduser("~/.zshrc")) as f:
        for line in f:
            if "N8N_API_KEY" in line and "export" in line:
                key = line.split("=", 1)[1].strip().strip('"').strip("'"); break

def get(wid):
    r = urllib.request.Request(f"https://automation.landingpro.by/api/v1/workflows/{wid}",
        headers={"X-N8N-API-KEY": key, "Accept": "application/json"})
    return json.loads(urllib.request.urlopen(r, context=ctx, timeout=15).read())

for wid, label in [("3nkqIaVphDT3wDOk", "FC_ColdEmail_Scheduler"), ("H8YOY2gf3rZANXFl", "FC_ManualSend")]:
    print(f"\n=== {label}  ({wid}) ===")
    wf = get(wid)
    print(f"active: {wf.get('active')}  nodes: {len(wf['nodes'])}")
    for n in wf["nodes"]:
        t = n.get("type", "")
        if "email" in t.lower() or "mail" in t.lower():
            p = n.get("parameters", {})
            print(f"  [{n['name']}]  type={t}  emailType={p.get('emailType')}  hasHtml={'html' in p}  hasText={'text' in p}")
        elif t == "n8n-nodes-base.code":
            code = n["parameters"].get("jsCode", "")
            has_html = "wrapBranded" in code or "<html" in code or "<div" in code
            has_text = "text:" in code
            print(f"  [{n['name']}]  type=code  wrapBranded={has_html}  text_field={has_text}  len={len(code)}")
