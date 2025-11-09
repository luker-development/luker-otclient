# Luker OTClient

Public repository for the **Luker OTServer 15.03** client.  
This repository contains the full playable client, automatic version tracking, and tools used to generate launcher updates and GitHub releases.

---

## 📦 Installation (Players)

1. Download the latest release from the [Releases](https://github.com/luker-development/luker-otclient/releases) page.
2. Extract all files to a folder (e.g. `C:\Games\LukerOT\`).
3. Run `client.exe`.
4. In the login screen, connect to:
   ```
   Server: luker-otserver.ddns.net
   Port: 7171
   Version: 15.03
   ```

---

## 🧠 Development Notes

- This repository is **public** for distribution purposes.
- The **server** and its configuration remain private.
- The included script `generate_manifest.py` automates versioning, manifest creation, and GitHub release publishing.

---

## 🔄 Update & Build Workflow (Developers)

1. **Bump version and rebuild manifest:**
   ```bash
   python generate_manifest.py --bump
   ```
2. **Create a GitHub release automatically:**
   ```bash
   python generate_manifest.py --bump minor --release
   ```
3. The script will:
   - Update `updater/version.txt`
   - Rebuild `updater/manifest.json`
   - Create a ZIP in `updater/builds/`
   - Upload it to GitHub Releases

---

## 🧰 Folder Structure

```text
luker-otclient/
  bin/
  data/
  assets/
  conf/
  storeimages/
  updater/
    version.txt
    manifest.json
    patch_notes.txt
    builds/
  generate_manifest.py
  .gitattributes
  .gitignore
  README.md
```

---

## 🧩 Launcher Integration

The future **Luker Launcher** will:
1. Compare the local version against `updater/version.txt` on GitHub.
2. Download the corresponding ZIP build from the latest GitHub Release.
3. Extract and patch changed files automatically.
4. Display patch notes from `updater/patch_notes.txt`.

---

## 📜 License

This repository is intended for **client distribution and launcher integration**.  
All assets and content remain property of the **Luker OTServer** project.
