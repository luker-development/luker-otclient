# Luker OTClient

This repository contains the **public client** for the Luker OTServer (based on Tibia 15.03).  
It is designed to work with the future **Luker Launcher**, which will handle automatic updates, patching, and changelog display.

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

The **Luker Launcher** (to be developed next) will:
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

If you’re releasing a new build, follow this **every time**:

### 1️⃣ Bump version and regenerate manifest
```bash
python generate_manifest.py --bump
```
This will:
- Read the current version from `updater/version.txt`
- Bump the patch version (`1.0.0 → 1.0.1`)
- Recalculate file hashes
- Update `updater/manifest.json`
- Generate a ZIP containing only changed files inside `updater/builds/`

### 2️⃣ Publish release automatically
```bash
python generate_manifest.py --bump minor --release
```
This will:
- Do everything above
- Then use your `GITHUB_TOKEN` to create a **GitHub Release**
- Attach the `.zip` build as an asset for launcher or players

> 🔐 Note: Only your local environment variable `GITHUB_TOKEN` allows uploads.  
> If someone else clones this repo, the script still works locally but won’t upload.

---

## 🧰 Folder Structure (Explained for Future Luker)

```text
luker-otclient/
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

## 🔍 Script Reference – `generate_manifest.py`

### 🧠 What it does
- Reads your current version.
- Bumps it (patch/minor/major or specific).
- Rehashes all client files.
- Updates `manifest.json` automatically.
- Generates a ZIP of changed files.
- Optionally uploads the release to GitHub.

### 💡 Examples
```bash
python generate_manifest.py                # Only regenerate manifest
python generate_manifest.py --bump         # Bump patch (e.g., 1.0.0 → 1.0.1)
python generate_manifest.py --bump minor   # Bump minor version (1.0.0 → 1.1.0)
python generate_manifest.py --bump major   # Bump major version (1.0.0 → 2.0.0)
python generate_manifest.py --bump 1.3.5   # Set version manually
python generate_manifest.py --bump --release  # Full automated release
```

### 🔑 GitHub setup
You must have a personal token set locally:

```bash
setx GITHUB_TOKEN "ghp_yourtokenhere"
```

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
All game assets and content remain property of the **Luker OTServer** project.  
Created and maintained by **Luker (Luca Bigliano)**.

---

> 🧭 Remember, Future Luker:
> This repo is your **public delivery channel**.  
> It doesn’t run the server, but it’s what players will download through your launcher.
> Keep it clean, predictable, and automated. You’ll thank yourself later.
