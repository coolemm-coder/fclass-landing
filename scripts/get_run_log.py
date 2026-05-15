#!/usr/bin/env python3
"""Download logs of failed FTP Sync step for run 25903525731."""
import os, json, urllib.request, sys, zipfile, io

RUN_ID = "25903525731"
REPO = "coolemm-coder/fclass-landing"

# Try with GITHUB_TOKEN if available
token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
headers = {"User-Agent": "claude", "Accept": "application/vnd.github+json"}
if token:
    headers["Authorization"] = f"Bearer {token}"

# Get jobs
req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/actions/runs/{RUN_ID}/jobs", headers=headers)
try:
    jobs = json.loads(urllib.request.urlopen(req).read())
except Exception as e:
    print("Jobs fetch error:", e)
    sys.exit(1)

for j in jobs["jobs"]:
    print("Job:", j["name"], "| log:", j.get("logs_url", "n/a"))

# Try to download logs zip
log_req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/actions/runs/{RUN_ID}/logs", headers=headers)
try:
    resp = urllib.request.urlopen(log_req)
    data = resp.read()
    print(f"\nDownloaded {len(data)} bytes")
    z = zipfile.ZipFile(io.BytesIO(data))
    for name in z.namelist():
        if "FTP Sync" in name or "ftp" in name.lower():
            print(f"\n=== {name} ===")
            content = z.read(name).decode("utf-8", errors="replace")
            # Last 60 lines
            lines = content.splitlines()
            for l in lines[-80:]:
                print(l)
except urllib.error.HTTPError as e:
    print(f"\nLog download HTTP error {e.code}: need GH token. Body: {e.read()[:200]}")
except Exception as e:
    print("Log download error:", e)
