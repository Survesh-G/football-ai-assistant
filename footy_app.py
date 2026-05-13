"""
PITCH IQ — Football Intelligence System v4
Fixes:
  - keyboard_double_arrow_right: DOM MutationObserver removes Streamlit's
    Material Icons <link> tag before it can load, preventing ligature rendering
  - User prompt leaking: display_text vs api_text pattern
  - Al Nassr / current data: stronger system prompt + llama-3.3-70b-versatile
  - Colours: Cyan / Red / White
  - Font: Inter + JetBrains Mono (system fallbacks in hero iframe)
"""

import streamlit as st
import requests
from datetime import datetime
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
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
# INJECT: MutationObserver script + CSS
#
# The keyboard_double_arrow_right text appears because Streamlit Cloud injects:
#   <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
# into <head> AFTER our page loads. Once that font loads, any element using
# the "Material Icons" font-family renders its text content as icon ligatures —
# and when those elements are briefly visible before the font maps them, or when
# CSS overrides interfere, the raw ligature name shows as text.
#
# The MutationObserver watches for that exact <link> being added to <head>
# and removes it instantly, before the font file is ever requested.
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* Keep your app fonts for normal text */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
}

/* But restore Streamlit material icons */
[data-testid="stIconMaterial"],
.material-symbols-rounded,
.material-icons {
    font-family: "Material Symbols Rounded", "Material Icons" !important;
    font-weight: normal !important;
    font-style: normal !important;
    display: inline-flex !important;
    align-items: center;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)
<script>
(function () {

  function removeMaterialIcons() {
    document.querySelectorAll('link').forEach(function (el) {
      const href = (el.href || "").toLowerCase();

      if (
        href.includes("materialicons") ||
        href.includes("material-icons") ||
        href.includes("material+icons") ||
        href.includes("fonts.googleapis.com/icon") ||
        href.includes("fonts.gstatic.com")
      ) {
        el.remove();
      }
    });
  }

  // Initial cleanup
  removeMaterialIcons();

  // Watch for new injected links
  const observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      mutation.addedNodes.forEach(function (node) {

        if (node.nodeType !== 1) return;

        // Direct LINK node
        if (node.tagName === "LINK") {
          const href = (node.href || "").toLowerCase();

          if (
            href.includes("material") ||
            href.includes("fonts.googleapis.com/icon") ||
            href.includes("fonts.gstatic.com")
          ) {
            node.remove();
          }
        }

        // Nested LINK nodes
        node.querySelectorAll?.("link").forEach(function (el) {
          const href = (el.href || "").toLowerCase();

          if (
            href.includes("material") ||
            href.includes("fonts.googleapis.com/icon") ||
            href.includes("fonts.gstatic.com")
          ) {
            el.remove();
          }
        });

      });
    });
  });

  observer.observe(document.documentElement, {
    childList: true,
    subtree: true
  });

})();
</script>
<style>
span.material-symbols-rounded {
    display: none !important;
}

i.material-icons {
    display: none !important;
}
</style>
<style>
/* Belt-and-suspenders: even if the font somehow loads, zero out all ligature text */
button[kind="header"] {
    font-family: inherit !important;
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

/* ── Hide avatar column in chat messages entirely ── */
[data-testid="stChatMessage"] > div:first-child {
    display: none !important;
}

.stChatMessage {
    background: #0a0e1a !important;
    border: 1px solid var(--b2) !important;
    border-radius: 6px !important;
    margin-bottom: 8px !important;
    padding: 14px 18px !important;
    gap: 0 !important;
}
[data-testid="stChatMessageContent"] p {
    color: var(--white) !important;
    line-height: 1.8 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
}
[data-testid="stChatMessageContent"] li {
    line-height: 1.7 !important;
    font-size: 14px !important;
    margin-bottom: 2px !important;
}
[data-testid="stChatMessageContent"] strong {
    color: var(--cyan) !important;
    font-weight: 700 !important;
}

/* user bubble — left cyan border */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    border-left: 2px solid var(--cyan) !important;
}
/* assistant bubble — left red border */
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
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
div[data-testid="stRadio"] label:hover { border-color: rgba(0,212,255,.3) !important; }
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
# HTML — STANDINGS TABLE
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
# messages stores the full API history (with enriched prompts).
# display_messages stores only what the user should see in the UI.
# ══════════════════════════════════════════════════════════════════════════════
if "selected_league"   not in st.session_state:
    st.session_state.selected_league = "EPL"
if "table_expanded"    not in st.session_state:
    st.session_state.table_expanded  = False

SYSTEM_PROMPT = """You are PITCH IQ — an elite football AI analyst.

CRITICAL KNOWLEDGE — always apply this:
- Cristiano Ronaldo left Manchester United in Nov 2022 and joined Al Nassr (Saudi Pro League) in Jan 2023. He is NOT at any European club.
- Lionel Messi joined Inter Miami (MLS) in July 2023. He is NOT at PSG or Barcelona.
- Neymar joined Al Hilal (Saudi Pro League) in Aug 2023.
- Kylian Mbappe joined Real Madrid in summer 2024 after leaving PSG on a free transfer.
- Erling Haaland is at Manchester City (joined 2022).
- Jude Bellingham is at Real Madrid (joined 2023).
- The Saudi Pro League (SPL) features Ronaldo (Al Nassr), Karim Benzema (Al Ittihad), Neymar (Al Hilal), Roberto Firmino (Al Ahli).
- Always confirm a player's current club before discussing their performance.

Your role: provide sharp tactical analysis, player breakdowns, club history, head-to-heads, transfer intel, and formation deep-dives. Be confident, opinionated — top pundit meets data scientist.

Format: **bold headers**, concise bullet points, short paragraphs.
Current season: {season}. Today: {today}."""

def build_system_prompt():
    return SYSTEM_PROMPT.format(
        season=SEASON_LABEL,
        today=now.strftime('%d %B %Y'),
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": build_system_prompt()}
    ]
# display_messages: list of {"role": "user"|"assistant", "content": str}
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

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
        "Ronaldo at Al Nassr",
        "Mbappe at Real Madrid",
        "Best pressing teams",
        "UCL dark horses",
        "4-3-3 vs 4-2-3-1",
    ]:
        st.markdown(f'<span class="pill">› {q}</span>', unsafe_allow_html=True)

    st.write("")
    if st.button("CLEAR CHAT", use_container_width=True):
        st.session_state.messages = [
            {"role": "system", "content": build_system_prompt()}
        ]
        st.session_state.display_messages = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# HERO — isolated iframe, no external fonts, no Streamlit injection
# ══════════════════════════════════════════════════════════════════════════════
hero_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
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
.kicker{{font-family:Arial,sans-serif;font-size:8px;color:#1a3040;letter-spacing:4px;text-transform:uppercase;margin-bottom:10px;}}
.title{{font-family:'Arial Black',Arial,sans-serif;font-weight:900;font-size:48px;line-height:1;color:#f4f6fb;margin-bottom:8px;letter-spacing:-2px;}}
.hl  {{ color:#00d4ff; }}
.hl2 {{ color:#ff3154; }}
.sub{{font-family:'Courier New',monospace;font-size:9px;color:#1a3040;letter-spacing:.5px;margin-bottom:14px;}}
.badges{{display:flex;gap:8px;flex-wrap:wrap}}
.badge{{display:inline-flex;align-items:center;gap:5px;border-radius:3px;padding:3px 10px;font-family:'Courier New',monospace;font-size:8px;letter-spacing:1.2px;text-transform:uppercase;}}
.b1{{border:1px solid rgba(0,212,255,.25);color:#00d4ff;background:rgba(0,212,255,.04)}}
.b2{{border:1px solid rgba(255,49,84,.20);color:#ff3154;background:rgba(255,49,84,.04)}}
.b3{{border:1px solid rgba(244,246,251,.07);color:#4a5568;background:transparent}}
.dot{{width:5px;height:5px;border-radius:50%;background:#00d4ff;animation:p 1.8s ease-in-out infinite;display:inline-block;flex-shrink:0;}}
@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.1}}}}
.bg-num{{position:absolute;right:16px;bottom:-18px;font-family:'Arial Black',Arial,sans-serif;font-size:110px;font-weight:900;color:rgba(0,212,255,0.025);line-height:1;user-select:none;letter-spacing:-4px;}}
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
    <div class="badge b2">Groq &middot; Llama 3.3</div>
    <div class="badge b3">100% Free</div>
  </div>
  <div class="bg-num">IQ</div>
</div>
</body>
</html>"""

components.html(hero_html, height=172, scrolling=False)

# ══════════════════════════════════════════════════════════════════════════════
# CHAT HISTORY — render from display_messages only (clean, no prompt leakage)
# ══════════════════════════════════════════════════════════════════════════════
for dm in st.session_state.display_messages:
    with st.chat_message(dm["role"]):
        st.markdown(dm["content"])

# ══════════════════════════════════════════════════════════════════════════════
# CHAT INPUT
# ══════════════════════════════════════════════════════════════════════════════
user_input = st.chat_input("Ask anything — tactics, transfers, history, players...")

if user_input:
    # 1. Show the raw user text immediately
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.display_messages.append(
        {"role": "user", "content": user_input}
    )

    # 2. Build enriched prompt for API (standings context injected here)
    live_ctx = ""
    if sdata:
        lines = [
            f"{t['rank']}. {t['name']} — {t['pts']}pts "
            f"({t['w']}W {t['d']}D {t['l']}L GD:{t['gd']})"
            for t in sdata[:5]
        ]
        live_ctx = (
            f"\n\n[Context — {sel['name']} Top 5 as of {now.strftime('%d %b %Y')}]\n"
            + "\n".join(lines)
            + "\n[End context]"
        )

    api_prompt = (
        f"{user_input}{live_ctx}\n\n"
        "Respond as PITCH IQ. Use live context if relevant. "
        "Apply your current knowledge of player clubs — e.g. Ronaldo is at Al Nassr, "
        "Messi at Inter Miami, Mbappe at Real Madrid."
    )

    # 3. Append enriched version to API history
    st.session_state.messages.append({"role": "user", "content": api_prompt})

    # 4. Call Groq
    with st.chat_message("assistant"):
        with st.spinner("Analysing..."):
            try:
                from groq import Groq
                client = Groq(api_key=groq_api_key)
                resp   = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",   # latest, best factual recall
                    messages=st.session_state.messages,
                    temperature=0.35,
                    max_tokens=1200,
                )
                reply = resp.choices[0].message.content
            except Exception as e:
                reply = (
                    "**Connection Error**\n\n"
                    f"Ensure `GROQ_API_KEY` is set in Streamlit secrets.\n\n`{e}`"
                )
        st.markdown(reply)

    # 5. Append clean reply to both histories
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.display_messages.append({"role": "assistant", "content": reply})