"""Observatory tic-tac-toe: humanity (X) vs a perfect minimax AI (O).

Modes:
  python ttt.py render          re-render assets + README from current state
  python ttt.py reset           fresh board, keep stats
  python ttt.py move            apply move from ISSUE_TITLE / ISSUE_USER env
Writes a reply for the issue to .github/game/comment.txt (move mode).
"""
import json, os, random, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
STATE = os.path.join(ROOT, ".github", "game", "ttt-state.json")
COMMENT = os.path.join(ROOT, ".github", "game", "comment.txt")
CELLS = os.path.join(ROOT, "assets", "ttt")
README = os.path.join(ROOT, "README.md")
RAW = "https://raw.githubusercontent.com/AhmedTheNetCoder/AhmedTheNetCoder/main"
ISSUE_NEW = "https://github.com/AhmedTheNetCoder/AhmedTheNetCoder/issues/new"

WINS = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def load():
    if os.path.exists(STATE):
        with open(STATE, encoding="utf-8") as f:
            return json.load(f)
    return {"board":[" "]*9, "stats":{"human":0,"ai":0,"draw":0}, "recent":[],
            "moves":0, "finished":False, "highlight":[],
            "msg":"YOUR MOVE, EARTHLING — HUMANITY PLAYS X", "tone":"cyan"}

def save(st):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w", encoding="utf-8") as f:
        json.dump(st, f, indent=2)

def winner(b):
    for w in WINS:
        if b[w[0]] != " " and b[w[0]] == b[w[1]] == b[w[2]]:
            return b[w[0]], list(w)
    return None, []

def minimax(b, turn, depth=0):
    """Score from O's perspective. Returns (score, best_moves)."""
    win, _ = winner(b)
    if win == "O": return 10 - depth, []
    if win == "X": return depth - 10, []
    if " " not in b: return 0, []
    best, moves = None, []
    for i in range(9):
        if b[i] != " ": continue
        b[i] = turn
        s, _ = minimax(b, "X" if turn == "O" else "O", depth + 1)
        b[i] = " "
        better = (best is None or (turn == "O" and s > best) or (turn == "X" and s < best))
        if better:
            best, moves = s, [i]
        elif s == best:
            moves.append(i)
    return best, moves

# ── SVG rendering ────────────────────────────────────────────────
def cell_svg(mark, idx, hl):
    border = "#4ade80" if hl else "#263143"
    bw = "3" if hl else "1.5"
    body = ""
    if mark == "X":
        body = """
  <g stroke="#22d3ee" stroke-width="7" stroke-linecap="round" filter="url(#g)">
    <line x1="34" y1="34" x2="86" y2="86"/><line x1="86" y1="34" x2="34" y2="86"/>
  </g>
  <g fill="#e0f2fe"><circle cx="34" cy="34" r="3.4"/><circle cx="86" cy="86" r="3.4"/>
  <circle cx="86" cy="34" r="3.4"/><circle cx="34" cy="86" r="3.4"/></g>"""
    elif mark == "O":
        body = """
  <circle cx="60" cy="60" r="24" stroke="#a78bfa" stroke-width="7" filter="url(#g)"/>
  <ellipse cx="60" cy="60" rx="38" ry="10" transform="rotate(-18 60 60)" stroke="#f472b6" stroke-opacity="0.65" stroke-width="3"/>"""
    else:
        body = """
  <g fill="#e2e8f0" opacity="0.4"><circle cx="26" cy="24" r="1.2"/><circle cx="96" cy="88" r="1.2"/><circle cx="88" cy="30" r="1"/></g>
  <g stroke="#22d3ee" stroke-width="3" stroke-linecap="round" opacity="0.4">
    <line x1="60" y1="48" x2="60" y2="72"/><line x1="48" y1="60" x2="72" y2="60"/>
    <animate attributeName="opacity" values="0.22;0.55;0.22" dur="3s" repeatCount="indefinite"/>
  </g>"""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="120" height="120" viewBox="0 0 120 120" fill="none" role="img" aria-label="sector {idx+1}: {'empty' if mark==' ' else mark}">
  <defs><filter id="g" x="-60%" y="-60%" width="220%" height="220%">
    <feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
  </filter></defs>
  <rect x="2" y="2" width="116" height="116" rx="16" fill="#0e141d" stroke="{border}" stroke-width="{bw}"/>{body}
</svg>
"""

TONES = {"cyan":"#22d3ee", "green":"#4ade80", "violet":"#a78bfa", "pink":"#f472b6"}

def status_svg(st):
    color = TONES.get(st["tone"], "#22d3ee")
    recent = "  ".join("@" + esc(u) for u in st["recent"]) or "awaiting first contact"
    s = st["stats"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="820" height="120" viewBox="0 0 820 120" fill="none" role="img" aria-label="game status">
  <rect x="1" y="1" width="818" height="118" rx="14" fill="#0e141d" stroke="#263143" stroke-width="1.5"/>
  <text x="30" y="34" font-family="'Consolas','Courier New',monospace" font-size="11" letter-spacing="4" fill="#64748b">HUMANITY  vs  THE OBSERVATORY AI</text>
  <text x="30" y="66" font-family="'Consolas','Courier New',monospace" font-size="19" font-weight="700" fill="{color}">{esc(st["msg"])}</text>
  <g font-family="'Consolas','Courier New',monospace" font-size="13">
    <text x="30" y="98" fill="#22d3ee">✕ HUMANITY {s["human"]}</text>
    <text x="185" y="98" fill="#a78bfa">◍ AI {s["ai"]}</text>
    <text x="285" y="98" fill="#94a3b8">≡ DRAWS {s["draw"]}</text>
    <text x="790" y="98" text-anchor="end" fill="#64748b">LATEST OBSERVERS: {recent}</text>
  </g>
</svg>
"""

def render(st):
    os.makedirs(CELLS, exist_ok=True)
    for i in range(9):
        with open(os.path.join(CELLS, f"cell{i}.svg"), "w", encoding="utf-8") as f:
            f.write(cell_svg(st["board"][i], i, i in st["highlight"]))
    with open(os.path.join(CELLS, "status.svg"), "w", encoding="utf-8") as f:
        f.write(status_svg(st))
    update_readme(st)

def update_readme(st):
    m = st["moves"]
    rows = []
    for r in range(3):
        tds = []
        for c in range(3):
            i = r * 3 + c
            img = f'<img src="{RAW}/assets/ttt/cell{i}.svg?m={m}" width="110" alt="sector {i+1}"/>'
            if st["board"][i] == " " or st["finished"]:
                body = ("Just press SUBMIT NEW ISSUE - you do not need to write anything. "
                        "The Observatory AI will move and close this issue in about 30 seconds. "
                        "Then refresh the profile to see the new board!")
                href = f"{ISSUE_NEW}?title=ttt%7Cmove%7C{i}&body=" + body.replace(" ", "+")
                tds.append(f'<td><a href="{href}">{img}</a></td>')
            else:
                tds.append(f"<td>{img}</td>")
        rows.append("<tr>" + "".join(tds) + "</tr>")
    section = f"""<div align="center">

<img src="{RAW}/assets/ttt/status.svg?m={m}" width="100%" alt="game status"/>

<table>
{chr(10).join(rows)}
</table>

</div>"""
    with open(README, encoding="utf-8") as f:
        txt = f.read()
    txt = re.sub(r"(<!--TTT:START-->).*?(<!--TTT:END-->)",
                 lambda mo: mo.group(1) + "\n" + section + "\n" + mo.group(2),
                 txt, flags=re.S)
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)

def write_comment(text):
    os.makedirs(os.path.dirname(COMMENT), exist_ok=True)
    with open(COMMENT, "w", encoding="utf-8") as f:
        f.write(text)

# ── main ─────────────────────────────────────────────────────────
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "move"
    st = load()

    if mode in ("render", "reset"):
        if mode == "reset":
            st.update(board=[" "]*9, finished=False, highlight=[],
                      msg="YOUR MOVE, EARTHLING — HUMANITY PLAYS X", tone="cyan")
            st["moves"] += 1
        save(st); render(st)
        return

    title = os.environ.get("ISSUE_TITLE", "")
    user = os.environ.get("ISSUE_USER", "someone")
    mt = re.match(r"^ttt\|move\|([0-8])$", title.strip())
    if not mt:
        write_comment("🛰️ Transmission garbled — I couldn't parse that move. "
                      "Please use the board links on the profile page.")
        print("::notice::unparseable title"); return
    idx = int(mt.group(1))

    if st["finished"]:  # start a new round with this move
        st.update(board=[" "]*9, finished=False, highlight=[])

    if st["board"][idx] != " ":
        write_comment(f"🛰️ Sector {idx+1} is already occupied, @{user}! "
                      "Head back to the [board](https://github.com/AhmedTheNetCoder) and pick a free sector.")
        print("::notice::occupied"); return

    st["board"][idx] = "X"
    st["recent"] = ([user] + [u for u in st["recent"] if u != user])[:3]
    st["moves"] += 1

    win, line = winner(st["board"])
    if win == "X":
        st["stats"]["human"] += 1
        st.update(finished=True, highlight=line, tone="green",
                  msg=f"IMPOSSIBLE?! HUMANITY WINS — SALUTE @{user.upper()}")
        reply = (f"🏆 **UNPRECEDENTED.** You beat the Observatory AI, @{user} — that is not supposed to be possible.\n\n"
                 "Your victory is now recorded on the scoreboard. Click any sector to start a new game.")
    elif " " not in st["board"]:
        st["stats"]["draw"] += 1
        st.update(finished=True, highlight=[], tone="violet",
                  msg="STALEMATE — THE UNIVERSE REMAINS IN BALANCE")
        reply = (f"⚖️ A draw, @{user} — the best possible outcome against a perfect machine. "
                 "Click any sector on the [board](https://github.com/AhmedTheNetCoder) to start a new game.")
    else:
        _, moves = minimax(st["board"], "O")
        ai = random.choice(moves)
        st["board"][ai] = "O"
        win, line = winner(st["board"])
        if win == "O":
            st["stats"]["ai"] += 1
            st.update(finished=True, highlight=line, tone="pink",
                      msg="THE OBSERVATORY AI WINS — RESISTANCE IS FUTILE")
            reply = (f"🤖 Checkmate-adjacent, @{user}. The AI takes sector {ai+1} and the round. "
                     "Click any sector on the [board](https://github.com/AhmedTheNetCoder) for a rematch — humanity needs you.")
        elif " " not in st["board"]:
            st["stats"]["draw"] += 1
            st.update(finished=True, highlight=[], tone="violet",
                      msg="STALEMATE — THE UNIVERSE REMAINS IN BALANCE")
            reply = (f"⚖️ A draw, @{user} — the best possible outcome against a perfect machine. "
                     "Click any sector on the [board](https://github.com/AhmedTheNetCoder) to start a new game.")
        else:
            st.update(tone="cyan", msg="YOUR MOVE, EARTHLING — HUMANITY PLAYS X")
            reply = (f"📡 Move received, @{user}! You took sector {idx+1}; the AI answered with sector {ai+1}.\n\n"
                     "Head back to the [board](https://github.com/AhmedTheNetCoder) — humanity awaits its next move.")
    save(st); render(st); write_comment(reply)
    print(f"move ok: human {idx}, finished={st['finished']}")

if __name__ == "__main__":
    main()
