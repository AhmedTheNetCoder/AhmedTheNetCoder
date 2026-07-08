# 🛰️ Observatory Deployment Manual

Everything you need to launch the Cosmic Data Observatory on your GitHub profile.

## 0. The one weird trick that makes a profile README exist
GitHub renders the README of a repo **named exactly like your username** at the
top of your profile page. For you that means a repo called:

```
AhmedTheNetCoder/AhmedTheNetCoder
```

## 1. Create the special repo
1. Go to https://github.com/new
2. **Repository name:** `AhmedTheNetCoder`  ← must match your username exactly
3. Set it **Public**, tick **Add a README**, create.
4. You'll see a banner: *"AhmedTheNetCoder/AhmedTheNetCoder is a special repository."* 🎉

## 2. Add the files
Copy this folder's contents into that repo, preserving structure:

```
AhmedTheNetCoder/
├── README.md
├── assets/
│   ├── header.svg
│   ├── divider.svg
│   └── gallery/            (your photos go here, optional)
└── .github/
    └── workflows/
        └── snake.yml
```

Easiest path (web UI):
- Open the repo → **Add file → Upload files** → drag `README.md`.
- Repeat for `assets/header.svg` and `assets/divider.svg` (create the `assets`
  folder by typing `assets/header.svg` as the filename when using *Create new file*).
- For the workflow: **Add file → Create new file** → name it
  `.github/workflows/snake.yml` → paste the contents.

Git path:
```bash
git clone https://github.com/AhmedTheNetCoder/AhmedTheNetCoder.git
# copy the files in, then:
git add .
git commit -m "Launch: Cosmic Data Observatory"
git push
```

## 3. Turn on the contribution snake 🐍
1. In the repo go to **Actions** → enable workflows if prompted.
2. Open **Generate Contribution Snake** → **Run workflow** (manual trigger).
3. It creates an `output` branch with `snake.svg`. The README already points at:
   `raw.githubusercontent.com/AhmedTheNetCoder/AhmedTheNetCoder/output/snake.svg`
4. It re-runs automatically twice a day. If the image is broken at first, just
   run the workflow once manually — the `output` branch doesn't exist until then.

## 4. Fill in the placeholders (5-minute pass)
Search the README for these and replace:
- **Long-Exposure Gallery** — swap the 3 placeholder badges for real photos.
  Trick: open any GitHub Issue, drag a photo into the comment box, copy the
  generated `https://...githubusercontent.com/...` URL, paste it as the `src`.
  Or drop files in `assets/gallery/` and use `./assets/gallery/name.jpg`.
- **Open a Channel** — set real URLs on the LinkedIn / Portfolio / 500px badges
  (they're currently `href="#"`).
- **First Contact** — tweak the `yaml` block wording to taste.

## 5. Optional upgrades
- **Spotify now-playing:** add a `natemoo-re/spotify-readme` or
  `kittinan/spotify-github-profile` card under Telemetry.
- **WakaTime coding stats:** sign up at wakatime.com, add the weekly-stats card.
- **Light/dark banner:** duplicate `header.svg` as a light variant and wrap both
  in a `<picture>` element with `media="(prefers-color-scheme: light/dark)"`.

## 6. Verify it animates
Open `assets/header.svg` directly in a browser — stars should twinkle, the planet
should orbit, a shooting star should streak. GitHub serves SVGs as images, so the
SMIL animations play on your profile too. If motion ever looks frozen in the README
preview, hard-refresh (Ctrl+F5) — GitHub's image proxy caches aggressively.

---
Pro tip: after everything's live, run every stats URL once by visiting your
profile — the Vercel cards cold-start on first hit and load instantly after.
