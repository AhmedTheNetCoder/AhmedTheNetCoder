#!/usr/bin/env bash
# Regenerate assets/transmission.svg — quote of the day, rotated by day-of-year.
set -euo pipefail
cd "$(dirname "$0")/../.."

QUOTES="assets/quotes.txt"
OUT="assets/transmission.svg"

count=$(grep -c '|' "$QUOTES")
doy=$((10#$(date -u +%j)))
idx=$(( (doy % count) + 1 ))
line=$(sed -n "${idx}p" "$QUOTES")
quote=${line%%|*}
author=${line##*|}

esc() { local s=$1; s=${s//&/&amp;}; s=${s//</&lt;}; s=${s//>/&gt;}; printf '%s' "$s"; }
quote=$(esc "$quote")
author=$(esc "$author")

cat > "$OUT" <<EOF
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="88" viewBox="0 0 1200 88" fill="none" role="img" aria-label="Transmission of the day">
  <rect x="1" y="1" width="1198" height="86" rx="14" fill="#0e141d" stroke="#263143" stroke-width="1.5"/>
  <g transform="translate(34,30)">
    <rect x="0"  y="10" width="5" height="18" rx="2.5" fill="#22d3ee">
      <animate attributeName="height" values="8;22;8" dur="1.1s" repeatCount="indefinite"/>
      <animate attributeName="y" values="20;6;20" dur="1.1s" repeatCount="indefinite"/>
    </rect>
    <rect x="10" y="4" width="5" height="24" rx="2.5" fill="#a78bfa">
      <animate attributeName="height" values="24;10;24" dur="1.3s" repeatCount="indefinite"/>
      <animate attributeName="y" values="4;18;4" dur="1.3s" repeatCount="indefinite"/>
    </rect>
    <rect x="20" y="12" width="5" height="16" rx="2.5" fill="#f472b6">
      <animate attributeName="height" values="14;26;14" dur="0.9s" repeatCount="indefinite"/>
      <animate attributeName="y" values="16;2;16" dur="0.9s" repeatCount="indefinite"/>
    </rect>
  </g>
  <text x="78" y="34" font-family="'Consolas','Courier New',monospace" font-size="11" letter-spacing="3" fill="#64748b">TRANSMISSION OF THE DAY // DAY ${doy}</text>
  <text x="78" y="62" font-family="Georgia,'Times New Roman',serif" font-size="19" font-style="italic" fill="#c9d1d9">&#8220;${quote}&#8221;</text>
  <text x="1166" y="62" text-anchor="end" font-family="'Consolas','Courier New',monospace" font-size="13" fill="#a78bfa">&#8212; ${author}</text>
</svg>
EOF
echo "transmission: day ${doy} -> quote ${idx}/${count} (${author})"
