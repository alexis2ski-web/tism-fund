# tism fund

Installable web app for Alexis's NHL and NFL picks, fantasy matchups and bet builder.

- `index.html` – the app (same page as the claude.ai version, reading `data.json` instead of the claude.ai database)
- `data.json` – picks, headlines and fantasy sheets, refreshed by the daily sync
- `sw.js`, `manifest.webmanifest`, `icons/` – what makes it installable and usable offline
- `tools/build_data.py` – builds `data.json` from the site's database export

Changes are made by asking Claude in the "Sport betting tool" project; every change is a commit, so any version can be restored.
