# Argentibia OTClient

This repository contains the **public client** for the Argentibia OTServer (based on Tibia 15.03).  
It is designed to work with the future **Argentibia Launcher**, which will handle automatic updates, patching, and changelog display.

Everything here is safe for public distribution — no server credentials or internal Lua files are exposed.  
Think of this as the *“downloadable game client”* repository.

---

## ⚙️ Purpose of This Repository

This repo serves three main goals:

1. **Distribute the client** publicly through GitHub Releases.
2. **Maintain version tracking and patch manifests** for launcher integration.
3. **Automate builds and release uploads** through a single script (`generate_manifest.py`).

If you (Future Luker) ever forget why this repo exists:  
👉 this is the *public-facing build system* for players, separate from the private server repository.

---

## 🧩 Launcher Integration Overview

The **Argentibia Launcher** (to be developed next) will:
1. Fetch the latest version from  
   `https://raw.githubusercontent.com/luker-development/luker-otclient/main/updater/version.txt`
2. Compare it to the local client version.
3. If newer, download the corresponding `.zip` build from the **latest GitHub Release**.
4. Extract only changed files (using `manifest.json` hashes).
5. Display `patch_notes.txt` as the update changelog.

This allows you to publish new client updates in minutes — no manual uploads, no confusion.

---

## 📦 Installation (Players)

1. Go to the [Releases page](https://github.com/luker-development/luker-otclient/releases).
2. Download the latest `.zip` version (example: `luker-otclient_1.0.0.zip`).
3. Extract all files to a folder (e.g., `C:\Games\LukerOT\`).
4. Run `client.exe`.
5. On login, use:
   ```
   Server: luker-otserver.ddns.net
   Port: 7171
   Version: 15.03
   ```

---

## 🔁 Developer Workflow (How to Publish Updates)

If you're releasing a new build, follow this **simple 3-step process**:

### 1️⃣ Update the version file
Edit `updater/version.txt` with your new version:
```bash
echo "1.0.2" > updater/version.txt
```

### 2️⃣ Commit and push to main
```bash
git add updater/version.txt
git commit -m "Release version 1.0.2"
git push origin main
```

### 3️⃣ Create a git tag and push it
```bash
git tag v1.0.2
git push origin v1.0.2
```

**That's it!** GitHub Actions will automatically:
- ✅ Verify version.txt matches the tag
- ✅ Create a ZIP of the client (excluding screenshots, cache, logs, debug files)
- ✅ Create a GitHub release with the ZIP attached
- ✅ Launcher detects the new version and prompts users to update

> 📝 **Version Format:** Use semantic versioning (major.minor.patch) for both `version.txt` and git tags.
> Example: `1.0.2` in version.txt → `git tag v1.0.2`

---4

## 🧰 Folder Structure (Explained for Future Luker)

```text
argentibia-otclient/
│
├── bin/                  → The compiled client and dependencies (.exe, .dll)
├── data/                 → Game data, modules, maps, UI, etc.
├── assets/               → Textures, icons, images, and static resources
├── conf/                 → Configuration files for the client
├── storeimages/          → Visuals for in-game store or effects
│
├── updater/
│   ├── version.txt       → Current client version
│   ├── manifest.json     → List of all files + their SHA1 hashes
│   ├── patch_notes.txt   → Displayed changelog for the launcher
│   └── builds/           → Generated ZIP builds for each release
│
├── generate_manifest.py  → Script that handles versioning, manifest, and GitHub releases
├── .gitattributes        → Git LFS settings for large files (dll, exe, dat, spr, etc.)
├── .gitignore            → Files/folders excluded from commits
└── README.md             → (This file) The full documentation for this repository
```

---

## 🔍 GitHub Actions Automation

The `.github/workflows/release.yml` file automatically handles releases when you push a git tag.

**What it does:**
- ✅ Verifies `version.txt` matches the tag
- ✅ Creates a ZIP archive (excludes screenshots, cache, logs, debug files)
- ✅ Creates a GitHub Release with the ZIP attached
- ✅ Launcher automatically detects and prompts users to update

No manual uploads, no scripts needed. Just push a tag and the workflow handles the rest.

---

## 🔧 Legacy: Script Reference – `generate_manifest.py`

This script is available but **no longer the primary workflow**. It was used for differential updates but is now replaced by GitHub Actions.

If you need to regenerate the manifest manually:
```bash
python generate_manifest.py                # Only regenerate manifest
```

> **Note:** The git tag workflow above is recommended for all releases.

---

## 🧱 How the Pieces Fit Together

| Component | Purpose |
|------------|----------|
| `version.txt` | Launcher checks this file to detect updates |
| `manifest.json` | Defines which files exist and their hashes for differential updates |
| `.zip build` | Actual downloadable client package for that version |
| `patch_notes.txt` | Launcher shows this text when updating |
| `generate_manifest.py` | Automates all the above, builds and publishes releases |

---

## 🧩 Roadmap

| Stage | Description | Status |
|--------|--------------|--------|
| 🧠 Client Repo Setup | Public repo, versioning, manifest | ✅ Done |
| ⚙️ Build Automation | Script to hash and upload new builds | ✅ Done |
| 🚀 Launcher | Cross-platform updater with progress bar and changelog display | 🔜 Next Step |
| 🎨 UI Polish | Custom launcher branding and theme integration | 🔜 Planned |

---

## 📜 License & Credits

This repository is intended for **client distribution and update automation** only.  
All game assets and content remain property of the **Argentibia OTServer** project.  
Created and maintained by **Luker (Luca Bigliano)**.

---

> 🧭 Remember, Future Luker:
> This repo is your **public delivery channel**.  
> It doesn’t run the server, but it’s what players will download through your launcher.
> Keep it clean, predictable, and automated. You’ll thank yourself later.
