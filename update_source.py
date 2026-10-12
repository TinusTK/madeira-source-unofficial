#!/usr/bin/env python3
"""Build an AltStore/SideStore source.json for Madeira from its GitHub releases.

Each new release's IPA is downloaded once to read its bundle ID and version;
releases already in source.json are reused without downloading again.
"""
import json
import os
import plistlib
import re
import tempfile
import urllib.request
import zipfile

REPO = "willfaust/Madeira"
OUT = "source.json"
ICON = "https://avatars.githubusercontent.com/u/39139570?v=4"  # swap for a nicer icon if you like

API_HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "madeira-source"}
if os.environ.get("GITHUB_TOKEN"):
    API_HEADERS["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"


def get_json(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=API_HEADERS)) as r:
        return json.load(r)


def read_info_plist(ipa_url):
    with tempfile.NamedTemporaryFile(suffix=".ipa") as tmp:
        req = urllib.request.Request(ipa_url, headers={"User-Agent": "madeira-source"})
        with urllib.request.urlopen(req) as r:
            while chunk := r.read(1 << 20):
                tmp.write(chunk)
        tmp.flush()
        with zipfile.ZipFile(tmp.name) as z:
            name = next(n for n in z.namelist()
                        if re.fullmatch(r"Payload/[^/]+\.app/Info\.plist", n))
            return plistlib.loads(z.read(name))


def main():
    old = {}
    if os.path.exists(OUT):
        with open(OUT) as f:
            old = json.load(f)
    old_app = (old.get("apps") or [{}])[0]
    known = {v["downloadURL"]: v for v in old_app.get("versions", [])}
    bundle_id = old_app.get("bundleIdentifier")

    versions = []
    for rel in get_json(f"https://api.github.com/repos/{REPO}/releases?per_page=20"):
        if rel["draft"]:
            continue
        ipa = next((a for a in rel["assets"] if a["name"].endswith(".ipa")), None)
        if not ipa:
            continue
        url = ipa["browser_download_url"]
        if url in known:
            versions.append(known[url])
            continue
        info = read_info_plist(url)
        bundle_id = bundle_id or info["CFBundleIdentifier"]
        versions.append({
            "version": info.get("CFBundleShortVersionString", rel["tag_name"].lstrip("v")),
            "buildVersion": str(info.get("CFBundleVersion", "1")),
            "date": rel["published_at"],
            "localizedDescription": rel["body"] or rel["name"] or rel["tag_name"],
            "downloadURL": url,
            "size": ipa["size"],
            "minOSVersion": info.get("MinimumOSVersion", "17.0"),
        })

    versions.sort(key=lambda v: v["date"], reverse=True)  # newest first

    source = {
        "name": "Madeira (unofficial)",
        "subtitle": "Auto-built from willfaust/Madeira GitHub releases",
        "iconURL": ICON,
        "website": f"https://github.com/{REPO}",
        "apps": [{
            "name": "Madeira",
            "bundleIdentifier": bundle_id,
            "developerName": "Will Faust",
            "subtitle": "Windows PC games on iPhone",
            "localizedDescription": "Run x86-64 Windows PC games on iPhone via FEX-Emu + Wine + DXMT.",
            "iconURL": ICON,
            "tintColor": "#3B82F6",
            "appPermissions": {"entitlements": [], "privacy": {}},
            "versions": versions,
        }],
        "news": [],
    }

    if source != old:
        with open(OUT, "w") as f:
            json.dump(source, f, indent=2)
            f.write("\n")
        print(f"Wrote {OUT} with {len(versions)} version(s); latest {versions[0]['version'] if versions else 'none'}")
    else:
        print("No changes")


if __name__ == "__main__":
    main()
