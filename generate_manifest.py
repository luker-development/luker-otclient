import os
import hashlib
import json
import argparse
import zipfile
import requests
from pathlib import Path

# === CONFIGURATION ===
INCLUDE_DIRS = ["bin", "data", "assets", "conf", "storeimages"]
EXCLUDE = {"minimap", "screenshots", "logs", ".git", "updater", "__pycache__"}

MANIFEST_PATH = Path("updater/manifest.json")
VERSION_PATH = Path("updater/version.txt")
BUILDS_DIR = Path("updater/builds")

# === GITHUB CONFIG ===
GITHUB_REPO = "luker-development/luker-otclient"  # <-- change if needed

def hash_file(filepath):
    sha1 = hashlib.sha1()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            sha1.update(chunk)
    return sha1.hexdigest()

def get_all_files(base_dirs):
    files = []
    for base in base_dirs:
        if not os.path.exists(base):
            continue
        for root, dirs, filenames in os.walk(base):
            dirs[:] = [d for d in dirs if d not in EXCLUDE]
            for name in filenames:
                if name.startswith("."):
                    continue
                path = Path(root) / name
                files.append(path)
    return files

def read_version():
    if VERSION_PATH.exists():
        return VERSION_PATH.read_text(encoding="utf-8").strip()
    return "0.0.0"

def write_version(new_version):
    VERSION_PATH.parent.mkdir(parents=True, exist_ok=True)
    VERSION_PATH.write_text(new_version.strip() + "\n", encoding="utf-8")

def bump_version(current, bump_value):
    parts = current.split(".")
    while len(parts) < 3:
        parts.append("0")
    major, minor, patch = map(int, parts[:3])
    if bump_value == "major":
        major += 1
        minor, patch = 0, 0
    elif bump_value == "minor":
        minor += 1
        patch = 0
    elif bump_value == "patch":
        patch += 1
    else:
        return bump_value
    return f"{major}.{minor}.{patch}"

def load_previous_manifest():
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return {f["path"]: f["hash"] for f in json.load(f)["files"]}
    return {}

def generate_manifest(version):
    print(f"Generating manifest for version: {version}")
    all_files = get_all_files(INCLUDE_DIRS)
    manifest = {"version": version, "files": []}

    for f in sorted(all_files):
        manifest["files"].append({
            "path": str(f).replace("\\", "/"),
            "hash": hash_file(f)
        })

    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, "w", encoding="utf-8") as mf:
        json.dump(manifest, mf, indent=2)
    print(f"✅ Manifest updated: {MANIFEST_PATH}")
    return manifest

def package_changes(new_manifest, old_manifest, version):
    changed = []
    for entry in new_manifest["files"]:
        path, hash_val = entry["path"], entry["hash"]
        if old_manifest.get(path) != hash_val:
            changed.append(path)

    if not changed:
        print("🟢 No file changes detected — skipping zip creation.")
        return None

    BUILDS_DIR.mkdir(parents=True, exist_ok=True)
    zip_path = BUILDS_DIR / f"luker-otclient_{version}.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in changed:
            if not os.path.exists(f):
                continue
            zipf.write(f, arcname=f)
    print(f"📦 Build created: {zip_path} ({len(changed)} changed files)")
    return zip_path

def upload_release(zip_path, version):
    """Publish release + upload zip to GitHub"""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ No GITHUB_TOKEN found in environment variables.")
        return

    headers = {"Authorization": f"token {token}"}
    release_url = f"https://api.github.com/repos/{GITHUB_REPO}/releases"

    # Create release
    payload = {"tag_name": f"v{version}", "name": f"Luker OTClient v{version}", "body": f"Auto-generated build {version}", "draft": False, "prerelease": False}
    print("🚀 Creating GitHub release...")
    r = requests.post(release_url, headers=headers, json=payload)
    if r.status_code not in (200, 201):
        print(f"❌ Release creation failed: {r.status_code} {r.text}")
        return
    upload_url = r.json()["upload_url"].split("{")[0]

    # Upload ZIP as asset
    print("⬆️  Uploading ZIP asset...")
    with open(zip_path, "rb") as f:
        params = {"name": zip_path.name}
        upload_headers = headers | {"Content-Type": "application/zip"}
        ur = requests.post(upload_url, headers=upload_headers, params=params, data=f)
    if ur.status_code in (200, 201):
        print(f"✅ Release uploaded successfully: {zip_path.name}")
    else:
        print(f"❌ Asset upload failed: {ur.status_code} {ur.text}")

def main():
    parser = argparse.ArgumentParser(description="Generate OTClient manifest, package ZIP, and optionally publish GitHub release.")
    parser.add_argument("--bump", nargs="?", const="patch", help="Bump version: major | minor | patch | or specify exact version (e.g., 1.2.0)")
    parser.add_argument("--release", action="store_true", help="Upload ZIP as a GitHub Release asset")
    args = parser.parse_args()

    current_version = read_version()
    new_version = current_version

    if args.bump:
        new_version = bump_version(current_version, args.bump)
        write_version(new_version)
        print(f"📈 Version bumped: {current_version} → {new_version}")

    old_manifest = load_previous_manifest()
    new_manifest = generate_manifest(new_version)
    zip_path = package_changes(new_manifest, old_manifest, new_version)

    if args.release and zip_path:
        upload_release(zip_path, new_version)

    print("✅ Done.")

if __name__ == "__main__":
    main()
