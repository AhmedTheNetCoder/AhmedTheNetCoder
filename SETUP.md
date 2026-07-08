# 🛰️ Observatory Operations Manual

Everything powering the Cosmic Data Observatory profile
(`AhmedTheNetCoder/AhmedTheNetCoder`), and the opt-in add-ons you can enable.

## What's live and how it stays fresh

| Piece | Source | Refresh |
|-------|--------|---------|
| Animated hero banner | `assets/observatory.svg` (hand-built SMIL) | static file, always current |
| Tech tiles | `skillicons.dev` | live service |
| Photo gallery | `assets/gallery/*.jpg` | static files |
| Contribution snake | `.github/workflows/snake.yml` → `output` branch | every 12h |
| 3D contribution calendar | `.github/workflows/3d-contrib.yml` → `profile-3d-contrib/` | daily |
| Metrics dashboard | `.github/workflows/metrics.yml` → `assets/metrics.svg` | daily |
| Stats / streak / activity cards | vercel/demolab services | live services |

All three workflows also run on every push to `main`, and can be run by hand from
the **Actions** tab → pick the workflow → **Run workflow**.

## Colour gotcha (already fixed — don't reintroduce it)
In `snake.yml` the colours **must** keep their `#` (e.g. `color_snake=#8b5cf6`).
A literal `#` is safe inside a YAML `|` block scalar. Dropping the `#` produces
invalid CSS and the snake renders **black/invisible**.

---

# Opt-in add-ons

## A. Upgrade metrics with a personal token (more plugins)
The metrics workflow runs on the built-in `GITHUB_TOKEN`, which covers the current
plugins. A classic PAT unlocks extras (private-contribution stats, `plugin_topics`,
`plugin_stars`, `plugin_followup`, etc.) and higher rate limits.

1. https://github.com/settings/tokens → **Generate new token (classic)** → scopes
   `repo`, `read:org`, `read:user`. Copy it.
2. Repo → **Settings → Secrets and variables → Actions → New repository secret**
   → name `METRICS_TOKEN`, paste the value.
3. In `metrics.yml` change `token: ${{ secrets.GITHUB_TOKEN }}` →
   `token: ${{ secrets.METRICS_TOKEN }}`, then add any extra `plugin_*: yes` lines.

## B. WakaTime coding-time card
Shows real time-per-language bars. Needs a free WakaTime account + editor plugin.

1. Sign up at https://wakatime.com, install the WakaTime plugin in VS Code, code a bit.
2. WakaTime → **Settings → Account** → copy your **Secret API Key**.
3. Add repo secret `WAKATIME_API_KEY`.
4. Add this to `metrics.yml` (it already has your token wired):
   ```yaml
   plugin_wakatime: yes
   plugin_wakatime_token: ${{ secrets.WAKATIME_API_KEY }}
   plugin_wakatime_url: https://wakatime.com
   plugin_wakatime_sections: time, languages, editors, projects
   ```
   The next run folds it into `assets/metrics.svg` — no extra embed needed.

## C. Spotify "now playing" card
Reads your currently-playing track. **Free Spotify account is enough** — only the
*Web Playback SDK* needs Premium; this card just *reads* state via the Web API.

Your app (`MOAhmed GitHub App`, client `0c8db3e…`) is already created. Finish it:

1. Spotify dashboard → **Edit settings** → under **APIs used** tick **Web API**
   (you currently only have *Web Playback SDK*, which can't read the track).
2. Reveal and copy the **Client Secret**.
3. Mint a refresh token with the helper script (run `node spotify-token.js`,
   open the printed URL, click Agree — it prints your `refresh_token`). Keep the
   secret and token **out of git**.
4. Fork `github.com/novatorem/novatorem`, deploy it to Vercel, and add three env vars:
   `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REFRESH_TOKEN`.
5. Embed the deployed URL under Telemetry:
   ```html
   <img src="https://YOUR-APP.vercel.app/api/spotify" alt="now playing"/>
   ```
Development mode is fine — the card only reads your own account.

## D. Star-history chart
`https://api.star-history.com/svg?repos=OWNER/REPO&type=Date` renders a stargazer
line chart. It has a light background and needs repos with several stars to look
good — enable it once your projects gather stars, or wrap it in a `<picture>` if
you want a dark variant.

---

## Verify motion
Open `assets/observatory.svg` in a browser — stars twinkle, planets orbit, the
radar sweeps, a shooting star streaks. GitHub serves SVGs as images so the SMIL
animations play on the profile too. If anything looks frozen or stale in the
README, hard-refresh (Ctrl+F5) — GitHub's image proxy caches aggressively.
