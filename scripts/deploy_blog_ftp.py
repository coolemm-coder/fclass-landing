#!/usr/bin/env python3
"""Deploy blog HTML + images to fclass.by via FTP. Reads creds from fclass-landing/.env.
Usage: python3 deploy_blog_ftp.py <spec>
  spec is a semicolon-separated list of items: localpath:remotedir
  remotedir is one of: blog | images | root
"""
import os, sys, ftplib

BASE = "/Users/admin/Desktop/FirstClass_Automation"
ENV = os.path.join(BASE, "fclass-landing", ".env")

def load_env(path):
    env = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip().strip('"').strip("'")
    return env

def main():
    env = load_env(ENV)
    host = env.get("FTP_HOST")
    user = env.get("FTP_USER")
    pwd = env.get("FTP_PASS")
    if not (host and user and pwd):
        print("ERROR: missing FTP creds in .env. keys present:", list(env.keys()))
        sys.exit(1)

    items = []
    for part in sys.argv[1].split(";"):
        part = part.strip()
        if not part:
            continue
        local, kind = part.rsplit(":", 1)
        items.append((local, kind))

    dirmap = {"blog": "/blog/", "images": "/images/blog/", "root": "/"}

    ftp = ftplib.FTP()
    ftp.connect(host, 21, timeout=60)
    ftp.login(user, pwd)
    ftp.set_pasv(True)
    print("Connected to", host, "as", user)

    # ensure /images/blog exists
    for d in ("/images", "/images/blog"):
        try:
            ftp.mkd(d)
            print("created", d)
        except ftplib.error_perm:
            pass

    for local, kind in items:
        remotedir = dirmap[kind]
        fname = os.path.basename(local)
        ftp.cwd(remotedir)
        with open(local, "rb") as fh:
            ftp.storbinary("STOR " + fname, fh)
        print("uploaded", local, "->", remotedir + fname)
        ftp.cwd("/")

    ftp.quit()
    print("DONE")

if __name__ == "__main__":
    main()
