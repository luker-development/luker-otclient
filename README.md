# Luker OTClient

Public repository for the **Luker OTServer 15.03** client.  
This client is required to connect to the Luker OTServer and will later be used by the official **Luker Launcher** for automatic updates.

---

## 📦 Installation

1. Download the latest version from the [Releases](https://github.com/luker-development/luker-otclient/releases) page.
2. Extract all files to a folder (for example: C:\Games\LukerOT).
3. Run client.exe.
4. In the login screen, make sure you’re connecting to:

   Server: luker-otserver.ddns.net   (example)
   Port: 7171
   Version: 15.03

---

## 🔄 Updating

The launcher (coming soon) will automatically check:
- updater/version.txt → current client version
- updater/manifest.json → file list and hashes
- updater/patch_notes.txt → latest changelog

If you’re updating manually, you can also run:

git pull origin main

to fetch the latest client files.

---

## 🧠 Development Notes

- The client uses data files from data/things/ and configuration modules from data/modules/.
- Do **not** delete or rename these folders.
- Launcher integration will use GitHub Releases as a CDN for versioned patches.
- The .gitignore excludes only non-essential runtime data (like logs, minimap cache, and screenshots).

---

## 🧰 Folder Structure

```text
luker-otclient/
  bin/
    client.exe
    BattlEye/
    plugins/
    qt.conf
    resources/
  data/
    things/
    modules/
    minimap/
    configs/
  updater/
    version.txt
    manifest.json
    patch_notes.txt
  .gitignore
  README.md
```

---

## 🧩 Future Launcher Integration

The official Luker Launcher will:
1. Compare the local version.txt against the one on GitHub.
2. Download only changed files (based on the manifest.json hashes).
3. Display patch notes directly from patch_notes.txt.
4. Automatically back up old files before patching.

---

## 📜 License

This repository is intended for public client distribution.  
All game assets remain property of the Luker OTServer project.
