"""
PITCH IQ — Football Intelligence System
Fixes: Material Icons ghost | chat avatar text | legend colours | removed scorers/fixtures
Colours: Cyan / Red / White | Font: Inter + JetBrains Mono
"""

import streamlit as st
import requests
from datetime import datetime
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG  —  emoji favicon, no text that could trigger icon fonts
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PITCH IQ · Football Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# SEASON
# ══════════════════════════════════════════════════════════════════════════════
now          = datetime.now()
SEASON       = now.year if now.month >= 7 else now.year - 1
SEASON_LABEL = f"{SEASON}/{str(SEASON + 1)[-2:]}"

# ══════════════════════════════════════════════════════════════════════════════
# LEAGUE MAP
# ══════════════════════════════════════════════════════════════════════════════
LEAGUES = {
    "EPL":        {"name": "Premier League",  "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "espn": "eng.1",          "rel_start": 18},
    "La Liga":    {"name": "La Liga",          "flag": "🇪🇸",       "espn": "esp.1",          "rel_start": 18},
    "Bundesliga": {"name": "Bundesliga",       "flag": "🇩🇪",       "espn": "ger.1",          "rel_start": 16},
    "Serie A":    {"name": "Serie A",          "flag": "🇮🇹",       "espn": "ita.1",          "rel_start": 18},
    "Ligue 1":    {"name": "Ligue 1",          "flag": "🇫🇷",       "espn": "fra.1",          "rel_start": 16},
    "UCL":        {"name": "Champions League", "flag": "⭐",        "espn": "uefa.champions", "rel_start": 99},
}

ESPN_BASE = "https://site.api.espn.com/apis/v2/sports/soccer"
HEADERS   = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
}

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# KEY FIX: override Material Icons @font-face with empty src so the font never
# loads. This stops icon ligature names like "keyboard_double_arrow_right",
# "face", "smart_toy" from rendering as visible text strings.
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Nuke Material Icons so ligature names never render as text ── */
@font-face { font-family: 'Material Icons';          src: local(''); }
@font-face { font-family: 'Material Icons Outlined'; src: local(''); }
@font-face { font-family: 'Material Icons Round';    src: local(''); }
@font-face { font-family: 'Material Symbols Outlined'; src: local(''); }
@font-face { font-family: 'Material Symbols Rounded';  src: local(''); }
.material-icons,
.material-icons-outlined,
.material-icons-round,
.material-symbols-outlined,
.material-symbols-rounded,
[class*="material-icon"],
[class*="material-symbol"] {
    font-size: 0 !important;
    width: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
}

/* ── Our fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');

:root {
    --ink:    #05080f;
    --white:  #f4f6fb;
    --cyan:   #00d4ff;
    --red:    #ff3154;
    --orange: #ff8c00;
    --muted:  #4a5568;
    --b1:     rgba(0,212,255,0.10);
    --b2:     rgba(244,246,251,0.06);
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--cyan); border-radius: 2px; }

html, .stApp { background: var(--ink) !important; }
.stApp::before {
    content: '';
    position: fixed; inset: 0; pointer-events: none; z-index: 0;
    background:
        radial-gradient(ellipse 100% 40% at 50% 0%,   rgba(0,212,255,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 50%  30% at 100% 100%, rgba(255,49,84,0.03)  0%, transparent 60%);
}
header { background: transparent !important; }
.block-container {
    padding-top: .6rem !important;
    padding-bottom: 3rem !important;
    position: relative; z-index: 1;
    max-width: 900px !important;
}

*, body, h1,h2,h3,h4,p,div,span,label,li,td,th {
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #070b16 !important;
    border-right: 1px solid var(--b1) !important;
    min-width: 300px !important;
}

/* ── Chat: hide avatar images/icons entirely — they cause the face/smart_toy bug ── */
[data-testid="stChatMessage"] > div:first-child {
    display: none !important;
}

.stChatMessage {
    background: #0a0e1a !important;
    border: 1px solid var(--b2) !important;
    border-radius: 6px !important;
    margin-bottom: 8px !important;
    padding: 14px 16px !important;
    gap: 0 !important;
}
[data-testid="stChatMessageContent"] p {
    color: var(--white) !important;
    line-height: 1.8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}

/* Differentiate user vs assistant via border colour */
[data-testid="stChatMessage"][data-testid*="user"],
.stChatMessage:nth-of-type(odd) {
    border-left: 2px solid var(--cyan) !important;
}
.stChatMessage:nth-of-type(even) {
    border-left: 2px solid var(--red) !important;
}

/* ── Chat input ── */
.stChatInputContainer,
div[data-testid="stChatInputContainer"] {
    background: #0a0e1a !important;
    border: 1px solid rgba(0,212,255,0.20) !important;
    border-radius: 6px !important;
}
.stChatInputContainer textarea {
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    background: transparent !important;
}
.stChatInputContainer textarea::placeholder { color: var(--muted) !important; }

/* ── Radio pills ── */
div[data-testid="stRadio"] > div {
    display: flex !important; gap: 4px !important; flex-wrap: wrap !important;
}
div[data-testid="stRadio"] label {
    background: #0a0e1a !important;
    border: 1px solid var(--b2) !important;
    border-radius: 4px !important; padding: 5px 0 !important;
    cursor: pointer !important; font-size: 15px !important;
    flex: 1 !important; text-align: center !important; transition: all .15s !important;
}
div[data-testid="stRadio"] label:hover     { border-color: rgba(0,212,255,.3) !important; }
div[data-testid="stRadio"] label:has(input:checked) {
    background: rgba(0,212,255,.08) !important;
    border-color: var(--cyan) !important;
}

/* ── Standings table ── */
.stbl { width: 100%; border-collapse: collapse; font-size: 11px; }
.stbl th {
    color: var(--muted) !important;
    font-weight: 600; padding: 6px 4px;
    text-align: center;
    border-bottom: 1px solid var(--b1);
    font-size: 9px; text-transform: uppercase; letter-spacing: 1.2px;
    font-family: 'JetBrains Mono', monospace !important;
}
.stbl th:nth-child(2) { text-align: left; }
.stbl td {
    padding: 5px 4px; text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    vertical-align: middle; font-size: 11px;
}
.stbl td:nth-child(2) { text-align: left; font-size: 11px; font-weight: 500; }
.stbl tr:hover td { background: rgba(0,212,255,.03); }

.pts  { color: var(--cyan)   !important; font-weight: 700 !important; font-family: 'JetBrains Mono', monospace !important; }
.gdp  { color: var(--cyan)   !important; font-family: 'JetBrains Mono', monospace !important; }
.gdn  { color: var(--red)    !important; font-family: 'JetBrains Mono', monospace !important; }
.rk   { color: var(--muted)  !important; font-family: 'JetBrains Mono', monospace !important; font-size: 10px !important; }
.rcl  { color: var(--cyan)   !important; font-weight: 700 !important; }
.rel  { color: var(--orange) !important; font-weight: 600 !important; }
.rrel { color: var(--red)    !important; font-weight: 600 !important; }

/* ── Section headers ── */
.section-hd {
    font-size: 8px !important; font-weight: 700 !important;
    color: var(--cyan) !important; letter-spacing: 3px !important;
    text-transform: uppercase !important; margin: 18px 0 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ── Pills ── */
.pill {
    display: inline-block; border: 1px solid var(--b2); border-radius: 3px;
    padding: 3px 9px; font-size: 10px !important; color: var(--muted) !important;
    margin: 2px; font-family: 'Inter', sans-serif !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important; border: 1px solid var(--b2) !important;
    color: var(--white) !important; border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 9px !important;
    letter-spacing: 1.5px !important; text-transform: uppercase !important;
    transition: all .2s !important; padding: 7px 12px !important;
}
.stButton > button:hover {
    border-color: var(--cyan) !important; color: var(--cyan) !important;
    background: rgba(0,212,255,0.05) !important;
}

hr { border-color: var(--b1) !important; margin: 14px 0 !important; }

.meta {
    font-size: 8px !important; color: var(--muted) !important;
    margin-top: 8px !important; font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: .5px;
}
.ldot {
    display: inline-block; width: 5px; height: 5px;
    background: var(--cyan); border-radius: 50%;
    animation: lp 1.8s ease-in-out infinite;
    vertical-align: middle; margin-right: 5px;
}
@keyframes lp { 0%,100%{opacity:1} 50%{opacity:.15} }

.nodata {
    font-size: 9px !important; color: var(--muted) !important;
    font-family: 'JetBrains Mono', monospace !important; letter-spacing: 1.5px;
    text-align: center; padding: 14px 0;
    border: 1px dashed #151c2e; border-radius: 4px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ESPN API — STANDINGS
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data(ttl=1800, show_spinner=False)
def espn_standings(league_code: str):
    try:
        r = requests.get(
            f"{ESPN_BASE}/{league_code}/standings",
            headers=HEADERS, timeout=12,
        )
        r.raise_for_status()
        data   = r.json()
        groups = data.get("children", []) or [data]
        entries = []
        for g in groups:
            for e in g.get("standings", {}).get("entries", []):
                team  = e.get("team", {})
                stats = {s["name"]: s.get("value", 0) for s in e.get("stats", [])}
                logos = team.get("logos", [])
                entries.append({
                    "rank": int(stats.get("rank", 0)),
                    "name": team.get("displayName", "—"),
                    "logo": logos[0].get("href", "") if logos else "",
                    "p":   int(stats.get("gamesPlayed", 0)),
                    "w":   int(stats.get("wins", 0)),
                    "d":   int(stats.get("ties", 0)),
                    "l":   int(stats.get("losses", 0)),
                    "gd":  int(stats.get("pointDifferential", 0)),
                    "pts": int(stats.get("points", 0)),
                })
        entries.sort(key=lambda x: x["rank"])
        return entries
    except Exception:
        return []

# ══════════════════════════════════════════════════════════════════════════════
# HTML — STANDINGS
# ══════════════════════════════════════════════════════════════════════════════
def standings_html(rows, rel_start: int, show_all: bool = False) -> str:
    if not rows:
        return '<div class="nodata">NO DATA · CHECK CONNECTION</div>'

    display = rows if show_all else rows[:5]
    body    = ""
    for t in display:
        rank = t["rank"]
        gd   = t["gd"]
        gds  = f"+{gd}" if gd > 0 else str(gd)
        gdc  = "gdp" if gd > 0 else ("gdn" if gd < 0 else "rk")

        if   rank <= 4:         rc = "rcl"
        elif rank <= 6:         rc = "rel"
        elif rank >= rel_start: rc = "rrel"
        else:                   rc = "rk"

        logo = t["logo"]
        nm   = (t["name"][:14] + "…") if len(t["name"]) > 14 else t["name"]
        logo_tag = (
            f'<img src="{logo}" width="13" height="13" '
            f'style="vertical-align:middle;margin-right:5px;border-radius:2px;opacity:.9">'
            if logo else ""
        )
        body += (
            f"<tr>"
            f'<td class="{rc}">{rank}</td>'
            f'<td>{logo_tag}{nm}</td>'
            f'<td style="font-family:JetBrains Mono,monospace">{t["p"]}</td>'
            f'<td style="font-family:JetBrains Mono,monospace">{t["w"]}</td>'
            f'<td style="font-family:JetBrains Mono,monospace">{t["d"]}</td>'
            f'<td style="font-family:JetBrains Mono,monospace">{t["l"]}</td>'
            f'<td class="{gdc}">{gds}</td>'
            f'<td class="pts">{t["pts"]}</td>'
            f"</tr>"
        )

    ts = now.strftime("%H:%M")

    # Use HTML entities for the square — avoids any icon font ligature risk
    legend = (
        '<p class="meta" style="margin-top:6px">'
        '<span style="color:#00d4ff">&#9632;</span>'
        '&nbsp;<span style="color:#4a5568;font-size:8px">UCL</span>'
        '&nbsp;&nbsp;'
        '<span style="color:#ff8c00">&#9632;</span>'
        '&nbsp;<span style="color:#4a5568;font-size:8px">UEL</span>'
        '&nbsp;&nbsp;'
        '<span style="color:#ff3154">&#9632;</span>'
        '&nbsp;<span style="color:#4a5568;font-size:8px">REL</span>'
        '</p>'
    )

    return (
        '<table class="stbl">'
        '<thead><tr>'
        '<th>#</th><th>CLUB</th><th>P</th><th>W</th>'
        '<th>D</th><th>L</th><th>GD</th><th>PTS</th>'
        '</tr></thead>'
        f'<tbody>{body}</tbody>'
        '</table>'
        f'<p class="meta"><span class="ldot"></span>ESPN · CACHED 30M · {ts}</p>'
        + legend
    )

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "selected_league" not in st.session_state:
    st.session_state.selected_league = "EPL"
if "table_expanded" not in st.session_state:
    st.session_state.table_expanded = False

SYSTEM_PROMPT = (
    "You are PITCH IQ — an elite football AI analyst with encyclopedic knowledge. "
    "Provide sharp tactical analysis, player breakdowns, club history, head-to-heads, "
    "transfer insights, and formation deep-dives. Be confident and opinionated — like a "
    "top pundit fused with a data scientist. Reference live data naturally when provided. "
    "Format responses with **bold headers** and concise bullet points. "
    f"Current season: {SEASON_LABEL}. Today: {now.strftime('%d %B %Y')}."
)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ══════════════════════════════════════════════════════════════════════════════
# API KEY
# ══════════════════════════════════════════════════════════════════════════════
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = None

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:

    # SVG logo — uses only system fonts inside SVG to avoid any icon font clash
    LOGO_SVG = """
    <div style="padding:20px 16px 4px">
      <svg width="200" height="60" viewBox="0 0 200 60" fill="none"
           xmlns="http://www.w3.org/2000/svg">
        <circle cx="28" cy="30" r="18" fill="none" stroke="#00d4ff"
                stroke-width="1.2" opacity=".65"/>
        <circle cx="28" cy="30" r="3.5" fill="#00d4ff" opacity=".95"/>
        <line x1="10" y1="30" x2="46" y2="30" stroke="#00d4ff"
              stroke-width=".7" opacity=".3"/>
        <line x1="28" y1="12" x2="28" y2="48" stroke="#00d4ff"
              stroke-width=".7" opacity=".3"/>
        <line x1="0"  y1="8"  x2="0"  y2="52" stroke="#00d4ff"
              stroke-width="2" opacity=".9"/>
        <text x="58" y="34" font-family="Arial Black, Arial, sans-serif"
              font-weight="900" font-size="22" fill="#f4f6fb"
              letter-spacing="-0.5">PITCH</text>
        <text x="59" y="50" font-family="Courier New, monospace"
              font-weight="700" font-size="9" fill="#00d4ff"
              letter-spacing="5">IQ  INTELLIGENCE</text>
      </svg>
    </div>
    """
    st.markdown(LOGO_SVG, unsafe_allow_html=True)

    st.markdown('<p class="section-hd">League Table</p>', unsafe_allow_html=True)
    selected_key = st.radio(
        "league",
        options=list(LEAGUES.keys()),
        format_func=lambda x: LEAGUES[x]["flag"],
        horizontal=True,
        key="selected_league",
        label_visibility="collapsed",
    )
    sel = LEAGUES[selected_key]

    st.markdown(
        f'<p style="font-size:9px;color:#1a3040;margin:4px 0 8px;'
        f'font-family:JetBrains Mono,monospace;letter-spacing:1px">'
        f'<span class="ldot"></span>{sel["name"].upper()} · {SEASON_LABEL}</p>',
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        sdata = espn_standings(sel["espn"])

    st.markdown(
        standings_html(sdata, sel["rel_start"], st.session_state.table_expanded),
        unsafe_allow_html=True,
    )

    total = len(sdata)
    if total > 5:
        btn_lbl = (
            "COLLAPSE TABLE" if st.session_state.table_expanded
            else f"SHOW ALL {total} CLUBS"
        )
        if st.button(btn_lbl, use_container_width=True, key="expand_btn"):
            st.session_state.table_expanded = not st.session_state.table_expanded
            st.rerun()

    st.divider()

    st.markdown(
        '<p style="font-size:7.5px;color:#1a2030;letter-spacing:2.5px;'
        'text-transform:uppercase;font-family:JetBrains Mono,monospace;'
        'margin-bottom:8px">Try Asking</p>',
        unsafe_allow_html=True,
    )
    for q in [
        "Messi vs Ronaldo",
        "Best pressing teams",
        "UCL dark horses",
        "Haaland analysis",
        "4-3-3 vs 4-2-3-1",
    ]:
        st.markdown(f'<span class="pill">› {q}</span>', unsafe_allow_html=True)

    st.write("")
    if st.button("CLEAR CHAT", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# HERO — isolated iframe via components.html
# Fully self-contained: no Streamlit CSS injection, no Material Icon fonts
# ══════════════════════════════════════════════════════════════════════════════
hero_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
/* NO external font imports here — keeps this iframe clean */
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:transparent;overflow:hidden;height:164px}}
.hero{{
  position:relative;height:164px;overflow:hidden;
  background:linear-gradient(135deg,#070b16 0%,#04060e 100%);
  border:1px solid rgba(0,212,255,0.10);border-radius:8px;
  padding:22px 30px 18px;
}}
.hero::before{{
  content:'';position:absolute;top:0;left:-100%;width:50%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(0,212,255,0.035),transparent);
  animation:scan 6s ease-in-out infinite;pointer-events:none;
}}
@keyframes scan{{0%{{left:-50%}}100%{{left:150%}}}}
.hero::after{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,#00d4ff,rgba(0,212,255,0.15) 60%,transparent);
}}
.side{{
  position:absolute;left:0;top:0;bottom:0;width:2px;
  background:linear-gradient(180deg,#00d4ff,rgba(0,212,255,0));
}}
.kicker{{
  font-family:Arial,sans-serif;font-size:8px;
  color:#1a3040;letter-spacing:4px;text-transform:uppercase;margin-bottom:10px;
}}
.title{{
  font-family:'Arial Black',Arial,sans-serif;font-weight:900;
  font-size:48px;line-height:1;color:#f4f6fb;
  margin-bottom:8px;letter-spacing:-2px;
}}
.hl  {{ color:#00d4ff; }}
.hl2 {{ color:#ff3154; }}
.sub{{
  font-family:'Courier New',monospace;font-size:9px;
  color:#1a3040;letter-spacing:.5px;margin-bottom:14px;
}}
.badges{{display:flex;gap:8px;flex-wrap:wrap}}
.badge{{
  display:inline-flex;align-items:center;gap:5px;
  border-radius:3px;padding:3px 10px;
  font-family:'Courier New',monospace;font-size:8px;
  letter-spacing:1.2px;text-transform:uppercase;
}}
.b1{{border:1px solid rgba(0,212,255,.25);color:#00d4ff;background:rgba(0,212,255,.04)}}
.b2{{border:1px solid rgba(255,49,84,.20);color:#ff3154;background:rgba(255,49,84,.04)}}
.b3{{border:1px solid rgba(244,246,251,.07);color:#4a5568;background:transparent}}
.dot{{
  width:5px;height:5px;border-radius:50%;background:#00d4ff;
  animation:p 1.8s ease-in-out infinite;display:inline-block;flex-shrink:0;
}}
@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.1}}}}
.bg-num{{
  position:absolute;right:16px;bottom:-18px;
  font-family:'Arial Black',Arial,sans-serif;font-size:110px;font-weight:900;
  color:rgba(0,212,255,0.025);line-height:1;user-select:none;letter-spacing:-4px;
}}
</style>
</head>
<body>
<div class="hero">
  <div class="side"></div>
  <div class="kicker">Football Intelligence System &nbsp;&middot;&nbsp; {SEASON_LABEL}</div>
  <div class="title">PITCH<span class="hl">I</span><span class="hl2">Q</span></div>
  <div class="sub">Standings &nbsp;&middot;&nbsp; Tactics &nbsp;&middot;&nbsp; Player Intel &nbsp;&middot;&nbsp; History</div>
  <div class="badges">
    <div class="badge b1"><span class="dot"></span>ESPN Live Data</div>
    <div class="badge b2">Groq &middot; Llama 3.1</div>
    <div class="badge b3">100% Free</div>
  </div>
  <div class="bg-num">IQ</div>
</div>
</body>
</html>"""

components.html(hero_html, height=172, scrolling=False)

# ══════════════════════════════════════════════════════════════════════════════
# CHAT HISTORY
# DO NOT pass avatar= to st.chat_message.
# Passing any string (emoji, symbol, letter) triggers Streamlit's avatar loader
# which maps it through the Material Icons font — causing "face"/"smart_toy"
# to appear as raw text. Omitting avatar= uses safe built-in silhouette icons.
# ══════════════════════════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ══════════════════════════════════════════════════════════════════════════════
# CHAT INPUT + PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
user_input = st.chat_input("Ask anything — tactics, transfers, history, players...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    live_ctx = ""
    if sdata:
        lines = [
            f"{t['rank']}. {t['name']} — {t['pts']}pts "
            f"({t['w']}W {t['d']}D {t['l']}L GD:{t['gd']})"
            for t in sdata[:5]
        ]
        live_ctx = (
            f"\n\nLive {sel['name']} Top 5 ({SEASON_LABEL}):\n"
            + "\n".join(lines)
        )

    prompt = (
        f"User Question: {user_input}{live_ctx}\n\n"
        "Answer as PITCH IQ. Reference live data naturally if relevant. "
        "Bold headers + bullet points. Be sharp, insightful, opinionated."
    )
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Analysing..."):
            try:
                from groq import Groq
                client = Groq(api_key=groq_api_key)
                resp   = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.38,
                    max_tokens=1024,
                )
                reply = resp.choices[0].message.content
            except Exception as e:
                reply = (
                    "**Connection Error**\n\n"
                    f"Ensure `GROQ_API_KEY` is set in Streamlit secrets.\n\n`{e}`"
                )
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})