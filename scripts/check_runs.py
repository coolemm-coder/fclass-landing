#!/usr/bin/env python3
import json, urllib.request
req = urllib.request.Request(
    "https://api.github.com/repos/coolemm-coder/fclass-landing/actions/runs?per_page=5",
    headers={"User-Agent": "claude"}
)
d = json.loads(urllib.request.urlopen(req).read())
for r in d["workflow_runs"]:
    print(r["head_sha"][:7], r["status"], r["conclusion"], r["created_at"], r.get("display_title", "")[:60])
