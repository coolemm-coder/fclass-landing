#!/usr/bin/env python3
import json, urllib.request, sys
req = urllib.request.Request(
    "https://api.github.com/repos/coolemm-coder/fclass-landing/actions/runs?per_page=1",
    headers={"User-Agent": "claude"}
)
d = json.loads(urllib.request.urlopen(req).read())
run = d["workflow_runs"][0]
print("SHA:", run["head_sha"][:7], "| status:", run["status"], "| conclusion:", run["conclusion"])
print("URL:", run["html_url"])
print("Run ID:", run["id"])
# Get jobs
jobs_req = urllib.request.Request(run["jobs_url"], headers={"User-Agent": "claude"})
jobs = json.loads(urllib.request.urlopen(jobs_req).read())
for j in jobs["jobs"]:
    print("\nJob:", j["name"], "| status:", j["status"], "| conclusion:", j["conclusion"])
    for step in j["steps"]:
        marker = "✅" if step["conclusion"] == "success" else ("❌" if step["conclusion"] == "failure" else "•")
        print(f"  {marker} {step['name']} -> {step['conclusion']}")
