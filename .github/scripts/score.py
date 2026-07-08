"""Global Observatory scoreboard: players transmit game results via issues.

Modes:
  python score.py render    re-render scoreboard SVG + README from state
  python score.py record    record result from ISSUE_TITLE / ISSUE_USER env
Writes the issue reply to .github/game/comment.txt (record mode).
"""
import json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STATE = os.path.join(ROOT, ".github", "game", "scoreboard.json")
COMMENT = os.path.join(ROOT, ".github", "game", "comment.txt")
SVG = os.path.join(ROOT, "assets", "scoreboard.svg")
README = os.path.join(ROOT, "README.md")
RAW = "https://raw.githubusercontent.com/AhmedTheNetCoder/AhmedTheNetCoder/main"
GAME = "https://ahmedthenetcoder.github.io/AhmedTheNetCoder/"

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def load():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    return {"win": 0, "draw": 0, "loss": 0, "recent": [], "n": 0}

def save(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)

RESULT_STYLE = {"win": ("#4ade80", "W"), "draw": ("#22d3ee", "D"), "loss": ("#f472b6", "L")}

def render(st):
    total = st["win"] + st["draw"] + st["loss"]
    if st["recent"]:
        parts = []
        for e in st["recent"][:5]:
            color, letter = RESULT_STYLE[e["r"]]
            name = e["u"] if len(e["u"]) <= 14 else e["u"][:13] + "…"
            parts.append(f'<tspan fill="#94a3b8">@{esc(name)}</tspan><tspan fill="{color}"> {letter}</tspan><tspan fill="#334155">   </tspan>')
        recent = "".join(parts)
    else:
        recent = '<tspan fill="#475569">awaiting first transmission…</tspan>'
    win_note = ('<text x="330" y="118" font-family="\'Consolas\',\'Courier New\',monospace" font-size="11" fill="#475569">'
                '* self-reported — the AI denies everything</text>') if st["win"] > 0 else ""
    star = "*" if st["win"] > 0 else ""
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="170" viewBox="0 0 1200 170" fill="none" role="img" aria-label="global scoreboard">
  <rect x="1" y="1" width="1198" height="168" rx="16" fill="#0e141d" stroke="#263143" stroke-width="1.5"/>
  <text x="34" y="38" font-family="'Consolas','Courier New',monospace" font-size="12" letter-spacing="4" fill="#64748b">GLOBAL OBSERVATORY SCOREBOARD — {total} TRANSMISSION{"S" if total != 1 else ""} RECEIVED FROM THE ARCADE</text>
  <g font-family="'Consolas','Courier New',monospace">
    <text x="34"  y="96" font-size="40" font-weight="700" fill="#a78bfa">{st["loss"]}</text>
    <text x="34"  y="118" font-size="12" letter-spacing="2" fill="#64748b">AI VICTORIES</text>
    <text x="200" y="96" font-size="40" font-weight="700" fill="#22d3ee">{st["draw"]}</text>
    <text x="200" y="118" font-size="12" letter-spacing="2" fill="#64748b">STALEMATES</text>
    <text x="366" y="96" font-size="40" font-weight="700" fill="#4ade80">{st["win"]}{star}</text>
    <text x="366" y="118" font-size="12" letter-spacing="2" fill="#64748b">HUMAN WINS</text>
    {win_note}
  </g>
  <line x1="560" y1="55" x2="560" y2="120" stroke="#263143" stroke-width="1.5"/>
  <text x="596" y="72" font-family="'Consolas','Courier New',monospace" font-size="12" letter-spacing="3" fill="#64748b">RECENT CHALLENGERS</text>
  <text x="596" y="100" font-family="'Consolas','Courier New',monospace" font-size="15">{recent}</text>
  <text x="596" y="128" font-family="'Consolas','Courier New',monospace" font-size="12" fill="#475569">play, then hit TRANSMIT RESULT to get your name here</text>
  <circle cx="1146" cy="36" r="5" fill="#4ade80"><animate attributeName="opacity" values="1;0.2;1" dur="2s" repeatCount="indefinite"/></circle>
  <text x="1136" y="41" text-anchor="end" font-family="'Consolas','Courier New',monospace" font-size="12" letter-spacing="2" fill="#64748b">LIVE</text>
</svg>
"""
    with open(SVG, "w", encoding="utf-8") as f:
        f.write(svg)
    section = (f'<p align="center">\n  <a href="{GAME}">\n'
               f'    <img src="{RAW}/assets/scoreboard.svg?v={st["n"]}" width="100%" alt="global scoreboard — live"/>\n'
               f'  </a>\n</p>')
    with open(README, encoding="utf-8") as f:
        txt = f.read()
    txt = re.sub(r"(<!--SCORE:START-->).*?(<!--SCORE:END-->)",
                 lambda m: m.group(1) + "\n" + section + "\n" + m.group(2), txt, flags=re.S)
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)

def write_comment(text):
    os.makedirs(os.path.dirname(COMMENT), exist_ok=True)
    with open(COMMENT, "w", encoding="utf-8") as f:
        f.write(text)

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "record"
    st = load()
    if mode == "render":
        save(st); render(st); return

    title = os.environ.get("ISSUE_TITLE", "")
    user = os.environ.get("ISSUE_USER", "someone")
    m = re.search(r"score\|(win|draw|loss)", title)
    if not m:
        write_comment("🛰️ Transmission garbled — I couldn't read that result. "
                      f"Please use the TRANSMIT RESULT button in the [arcade]({GAME}).")
        print("::notice::unparseable"); return
    res = m.group(1)
    st[res] += 1
    st["n"] += 1
    st["recent"] = ([{"u": user, "r": res}] + st["recent"])[:8]
    save(st); render(st)
    flavor = {
        "win":  f"🏆 A **claimed victory** from @{user} — logged with an asterisk, because the AI insists this is statistically impossible.",
        "draw": f"⚖️ Stalemate confirmed, @{user} — a perfect result against a perfect machine. Respect.",
        "loss": f"🤖 Defeat logged, @{user}. The Observatory AI thanks you for your contribution to its unbeaten record.",
    }[res]
    write_comment(flavor + "\n\nYour name is now on the "
                  "[global scoreboard](https://github.com/AhmedTheNetCoder) — "
                  f"current tallies: 🟣 {st['loss']} AI · 🔵 {st['draw']} draws · 🟢 {st['win']} human.\n\n"
                  f"Rematch any time in the [arcade]({GAME}).")
    print(f"recorded {res} by {user}")

if __name__ == "__main__":
    main()
