import streamlit as st
import requests
from datetime import datetime
import streamlit.components.v1 as components
import json

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PITCH IQ · Football Intelligence",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# SEASON
# ══════════════════════════════════════════════════════════════
now = datetime.now()
SEASON = now.year if now.month >= 7 else now.year - 1
SEASON_LABEL = f"{SEASON}/{str(SEASON + 1)[-2:]}"

# ══════════════════════════════════════════════════════════════
# ESPN API LEAGUE MAP  (free, no key, no rate limit)
# ══════════════════════════════════════════════════════════════
LEAGUES = {
    "EPL":        {"name": "Premier League",    "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "espn": "eng.1",  "rel_start": 18},
    "La Liga":    {"name": "La Liga",            "flag": "🇪🇸",       "espn": "esp.1",  "rel_start": 18},
    "Bundesliga": {"name": "Bundesliga",         "flag": "🇩🇪",       "espn": "ger.1",  "rel_start": 16},
    "Serie A":    {"name": "Serie A",            "flag": "🇮🇹",       "espn": "ita.1",  "rel_start": 18},
    "Ligue 1":    {"name": "Ligue 1",            "flag": "🇫🇷",       "espn": "fra.1",  "rel_start": 16},
    "UCL":        {"name": "Champions League",   "flag": "🌟",        "espn": "uefa.champions", "rel_start": 99},
}

ESPN_BASE = "https://site.api.espn.com/apis/v2/sports/soccer"
ESPN_SITE = "https://site.web.api.espn.com/apis/v2/sports/soccer"

# ══════════════════════════════════════════════════════════════
# GLOBAL CSS — FUTURISTIC HUD AESTHETIC
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --neon: #00ff87;
    --neon2: #00cfff;
    --accent: #ff3c6e;
    --bg: #030810;
    --panel: rgba(6,14,28,0.92);
    --border: rgba(0,255,135,0.12);
    --border2: rgba(0,207,255,0.10);
    --text: #e4eaf5;
    --muted: #4a5a72;
    --hud: rgba(0,255,135,0.06);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width:4px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--neon); border-radius:2px; }

/* ── Background ── */
.stApp {
    background: var(--bg) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,255,135,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(0,207,255,0.06) 0%, transparent 50%),
        repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(0,255,135,0.015) 40px),
        repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(0,255,135,0.015) 40px) !important;
    background-size: cover !important;
}

header { background:transparent !important; }
.block-container { padding-top:1rem !important; padding-bottom:2rem !important; }

/* ── Global text ── */
*, body, h1,h2,h3,h4,p,div,span,label,li,td,th {
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020a14 0%, #040d1a 100%) !important;
    border-right: 1px solid var(--border) !important;
    min-width: 300px !important;
    box-shadow: 4px 0 40px rgba(0,255,135,0.04) !important;
}
section[data-testid="stSidebar"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 300px; height: 2px;
    background: linear-gradient(90deg, transparent, var(--neon), transparent);
    z-index: 999;
}

/* ── Chat messages ── */
.stChatMessage {
    background: var(--panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    backdrop-filter: blur(20px) !important;
    margin-bottom: 10px !important;
    box-shadow: 0 0 20px rgba(0,255,135,0.03) !important;
}
[data-testid="stChatMessageContent"] p { color: var(--text) !important; line-height:1.7 !important; }

/* ── Chat input ── */
.stChatInputContainer {
    background: rgba(4,12,26,0.95) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    backdrop-filter: blur(20px) !important;
    box-shadow: 0 0 30px rgba(0,255,135,0.06), inset 0 0 20px rgba(0,255,135,0.02) !important;
}
.stChatInputContainer textarea {
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stChatInputContainer textarea::placeholder { color: var(--muted) !important; }

/* ── Radio pills ── */
div[data-testid="stRadio"] > div {
    display:flex !important; gap:4px !important; flex-wrap:wrap !important;
}
div[data-testid="stRadio"] label {
    background: rgba(0,255,135,0.04) !important;
    border: 1px solid rgba(0,255,135,0.12) !important;
    border-radius: 6px !important;
    padding: 4px 0 !important;
    cursor: pointer !important;
    font-size: 16px !important;
    flex: 1 !important;
    text-align: center !important;
    transition: all .2s !important;
    font-family: 'DM Sans', sans-serif !important;
}
div[data-testid="stRadio"] label:hover {
    background: rgba(0,255,135,0.10) !important;
    border-color: var(--neon) !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: rgba(0,255,135,0.15) !important;
    border-color: var(--neon) !important;
    box-shadow: 0 0 12px rgba(0,255,135,0.20) !important;
}

/* ── Standings table ── */
.stbl {
    width:100%; border-collapse:collapse;
    font-size:10.5px;
}
.stbl th {
    color: var(--muted) !important;
    font-weight:500; padding:4px 3px;
    text-align:center;
    border-bottom: 1px solid rgba(0,255,135,0.08);
    font-size:9px; text-transform:uppercase; letter-spacing:.6px;
}
.stbl th:nth-child(2) { text-align:left; }
.stbl td {
    padding:4px 3px; text-align:center;
    border-bottom: 1px solid rgba(255,255,255,0.02);
    vertical-align:middle;
}
.stbl td:nth-child(2) { text-align:left; }
.stbl tr:hover td { background: rgba(0,255,135,0.03); }
.pts  { color: var(--neon) !important; font-weight:700 !important; }
.gdp  { color: #00ff87 !important; }
.gdn  { color: #ff3c6e !important; }
.rcl  { color: #00ff87 !important; font-weight:700 !important; font-size:11px !important; }
.rel  { color: #ffaa00 !important; font-weight:600 !important; }
.rrel { color: #ff3c6e !important; font-weight:600 !important; }
.rank-num { font-size:10px !important; }

/* ── Scorers ── */
.sctbl { width:100%; border-collapse:collapse; font-size:11px; }
.sctbl td { padding:5px 3px; border-bottom:1px solid rgba(0,255,135,0.04); vertical-align:middle; }
.sc-rank  { color: var(--neon) !important; font-weight:700 !important; font-size:13px !important; width:18px; }
.sc-goals { color: var(--neon) !important; font-weight:700 !important; font-size:14px !important; text-align:right; }

/* ── Live badge ── */
.live-dot {
    display:inline-block; width:6px; height:6px;
    background: var(--neon); border-radius:50%;
    animation: livepulse 1.6s ease-in-out infinite;
    margin-right:5px; vertical-align:middle;
}
@keyframes livepulse {
    0%,100%{opacity:1;box-shadow:0 0 0 0 rgba(0,255,135,0.5)}
    50%{opacity:.5;box-shadow:0 0 0 5px rgba(0,255,135,0)}
}

/* ── Section headers ── */
.section-hd {
    font-size:9px !important; font-weight:600 !important;
    color: var(--neon) !important; letter-spacing:2px !important;
    text-transform:uppercase !important; margin-bottom:8px !important;
    font-family:'Orbitron',monospace !important;
}

/* ── Pills ── */
.pill {
    display:inline-block;
    background:rgba(0,255,135,0.05);
    border:1px solid rgba(0,255,135,0.15);
    border-radius:4px; padding:3px 9px;
    font-size:10.5px !important; color:#8fa8c0 !important;
    margin:2px; cursor:default;
    transition: all .2s;
}
.pill:hover { background:rgba(0,255,135,0.10) !important; color:var(--neon) !important; }

/* ── Buttons ── */
.stButton > button {
    background: rgba(0,255,135,0.05) !important;
    border: 1px solid rgba(0,255,135,0.20) !important;
    color: var(--neon) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size:12px !important;
    transition: all .2s !important;
    letter-spacing:.5px !important;
}
.stButton > button:hover {
    background: rgba(0,255,135,0.12) !important;
    box-shadow: 0 0 15px rgba(0,255,135,0.15) !important;
}

hr { border-color: rgba(0,255,135,0.08) !important; }
.meta { font-size:9px !important; color: #2a3a52 !important; margin-top:6px !important; }

/* ── Stat card ── */
.stat-card {
    background: rgba(0,255,135,0.04);
    border: 1px solid rgba(0,255,135,0.10);
    border-radius:8px; padding:8px 10px; margin:4px 0;
    display:flex; justify-content:space-between; align-items:center;
}
.stat-label { font-size:9px !important; color: var(--muted) !important; text-transform:uppercase; letter-spacing:.8px; }
.stat-value { font-size:14px !important; font-weight:700 !important; color: var(--neon) !important; }

/* Fix spinner */
.stSpinner { color: var(--neon) !important; }

/* Sidebar brand */
.brand {
    font-family:'Orbitron',monospace;
    font-size:20px; font-weight:900;
    color:#fff; letter-spacing:3px;
    text-align:center; margin:8px 0 4px;
}
.brand span { color: var(--neon); }
.brand-sub {
    font-size:8px !important; text-align:center !important;
    color: var(--muted) !important; letter-spacing:3px !important;
    text-transform:uppercase !important; margin-bottom:16px !important;
}

/* Match score pill */
.match-pill {
    background: rgba(0,207,255,0.06);
    border: 1px solid rgba(0,207,255,0.12);
    border-radius:6px; padding:5px 8px; margin:3px 0;
    font-size:11px;
}
.match-score { color: var(--neon2) !important; font-weight:700 !important; }
.match-team { color:#ccc !important; font-size:10.5px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# ESPN API HELPERS (free, no API key needed)
# ══════════════════════════════════════════════════════════════

@st.cache_data(ttl=1800, show_spinner=False)
def espn_standings(league_code: str):
    """Fetch standings from ESPN's free public API."""
    try:
        url = f"{ESPN_BASE}/{league_code}/standings"
        r = requests.get(url, timeout=10,
                         headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        data = r.json()
        groups = data.get("children", []) or [data]
        entries = []
        for g in groups:
            for e in g.get("standings", {}).get("entries", []):
                team = e.get("team", {})
                stats = {s["name"]: s.get("value", 0) for s in e.get("stats", [])}
                entries.append({
                    "rank":   int(stats.get("rank", 0)),
                    "name":   team.get("displayName", team.get("shortDisplayName", "—")),
                    "abbr":   team.get("abbreviation", ""),
                    "logo":   team.get("logos", [{}])[0].get("href", "") if team.get("logos") else "",
                    "p":      int(stats.get("gamesPlayed", 0)),
                    "w":      int(stats.get("wins", 0)),
                    "d":      int(stats.get("ties", 0)),
                    "l":      int(stats.get("losses", 0)),
                    "gf":     int(stats.get("pointsFor", 0)),
                    "ga":     int(stats.get("pointsAgainst", 0)),
                    "gd":     int(stats.get("pointDifferential", 0)),
                    "pts":    int(stats.get("points", 0)),
                })
        entries.sort(key=lambda x: x["rank"])
        return entries
    except Exception as ex:
        return []


@st.cache_data(ttl=900, show_spinner=False)
def espn_scoreboard(league_code: str):
    """Fetch recent/live scores from ESPN."""
    try:
        url = f"{ESPN_BASE}/{league_code}/scoreboard"
        r = requests.get(url, timeout=10,
                         headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        data = r.json()
        events = data.get("events", [])
        results = []
        for ev in events[:6]:
            comps = ev.get("competitions", [{}])[0]
                        # home/away
            competitors = comps.get("competitors", [])
            home = next((c for c in competitors if c.get("homeAway") == "home"), {})
            away = next((c for c in competitors if c.get("homeAway") == "away"), {})

            status = ev.get("status", {}).get("type", {})
            state  = status.get("state", "pre")   # pre / in / post
            detail = status.get("shortDetail", "")

            results.append({
                "home":    home.get("team", {}).get("shortDisplayName", "?"),
                "away":    away.get("team", {}).get("shortDisplayName", "?"),
                "hs":      home.get("score", "-"),
                "as_":     away.get("score", "-"),
                "state":   state,
                "detail":  detail,
            })
        return results
    except Exception:
        return []


@st.cache_data(ttl=1800, show_spinner=False)
def espn_top_scorers(league_code: str):
    """Fetch top scorers via ESPN leaders endpoint."""
    try:
        url = f"{ESPN_BASE}/{league_code}/leaders"
        r = requests.get(url, timeout=10,
                         headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        data = r.json()

        for cat in data.get("categories", []):
            if "goal" in cat.get("name", "").lower() or "goal" in cat.get("displayName","").lower():
                leaders = cat.get("leaders", [])[:5]
                results = []
                for l in leaders:
                    athlete = l.get("athlete", {})
                    team    = l.get("team", {})
                    results.append({
                        "name":  athlete.get("displayName", "—"),
                        "short": athlete.get("shortName", "—"),
                        "photo": athlete.get("headshot", {}).get("href", "") if isinstance(athlete.get("headshot"), dict) else "",
                        "team":  team.get("shortDisplayName", "—"),
                        "logo":  team.get("logos", [{}])[0].get("href", "") if team.get("logos") else "",
                        "goals": int(l.get("value", 0)),
                    })
                return results
        return []
    except Exception:
        return []


# ══════════════════════════════════════════════════════════════
# HTML BUILDERS
# ══════════════════════════════════════════════════════════════

def standings_html(rows, rel_start: int) -> str:
    if not rows:
        return (
            '<div style="text-align:center;padding:20px 0">'
            '<p style="color:#1a2a3a;font-size:11px;letter-spacing:1px">NO DATA · CHECK CONNECTION</p>'
            '</div>'
        )
    body = ""
    for t in rows:
        rank = t["rank"]
        gd   = t["gd"]
        gds  = f"+{gd}" if gd > 0 else str(gd)
        gdc  = "gdp" if gd > 0 else ("gdn" if gd < 0 else "")
        rc   = ("rcl" if rank <= 4
                else "rel" if rank <= 6
                else "rrel" if rank >= rel_start
                else "rank-num")
        logo = t["logo"]
        nm   = (t["name"][:14]+"…") if len(t["name"]) > 14 else t["name"]
        body += (
            f"<tr>"
            f'<td class="{rc}">{rank}</td>'
            f'<td>'
            + (f'<img src="{logo}" width="12" height="12" style="vertical-align:middle;margin-right:4px;border-radius:2px">' if logo else "")
            + f'{nm}</td>'
            f'<td>{t["p"]}</td><td>{t["w"]}</td><td>{t["d"]}</td><td>{t["l"]}</td>'
            f'<td class="{gdc}">{gds}</td>'
            f'<td class="pts">{t["pts"]}</td>'
            f"</tr>"
        )
    ts = now.strftime("%H:%M")
    return (
        '<table class="stbl">'
        '<thead><tr><th>#</th><th>Club</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GD</th><th>Pts</th></tr></thead>'
        f'<tbody>{body}</tbody></table>'
        f'<p class="meta"><span class="live-dot"></span>ESPN · auto-refresh 30m · {ts}</p>'
        '<p class="meta">'
        '<span style="color:#00ff87">■</span> UCL &nbsp;'
        '<span style="color:#ffaa00">■</span> UEL &nbsp;'
        '<span style="color:#ff3c6e">■</span> Relegation'
        '</p>'
    )


def scorers_html(data) -> str:
    if not data:
        return '<p style="color:#1a2a3a;font-size:10px;padding:10px 0;text-align:center">NO DATA AVAILABLE</p>'
    rows = ""
    for i, s in enumerate(data, 1):
        photo = s["photo"]
        name  = s["short"] if s["short"] != "—" else s["name"].split()[-1]
        tm    = (s["team"][:13]+"…") if len(s["team"]) > 13 else s["team"]
        logo  = s["logo"]
        rows += (
            f'<tr>'
            f'<td class="sc-rank">{i}</td>'
            f'<td>'
            + (f'<img src="{photo}" width="26" height="26" style="border-radius:50%;vertical-align:middle;margin-right:6px;object-fit:cover">' if photo else '<span style="display:inline-block;width:26px;height:26px;border-radius:50%;background:rgba(0,255,135,0.10);vertical-align:middle;margin-right:6px"></span>')
            + f'<span style="font-weight:600">{name}</span>'
            f'<br><span style="color:#2a4060;font-size:9.5px">'
            + (f'<img src="{logo}" width="10" height="10" style="vertical-align:middle;margin-right:2px">' if logo else "")
            + f'{tm}</span></td>'
            f'<td class="sc-goals">{s["goals"]}⚽</td>'
            f'</tr>'
        )
    return f'<table class="sctbl"><tbody>{rows}</tbody></table>'


def scoreboard_html(events) -> str:
    if not events:
        return ""
    out = ""
    for e in events:
        if e["state"] == "in":
            badge = f'<span style="color:#00ff87;font-size:8px;font-weight:700;letter-spacing:1px">● LIVE · {e["detail"]}</span>'
        elif e["state"] == "post":
            badge = f'<span style="color:#4a5a72;font-size:8px">FT · {e["detail"]}</span>'
        else:
            badge = f'<span style="color:#4a5a72;font-size:8px">{e["detail"]}</span>'

        out += (
            f'<div class="match-pill">'
            f'{badge}<br>'
            f'<span class="match-team">{e["home"]}</span> '
            f'<span class="match-score">{e["hs"]} – {e["as_"]}</span> '
            f'<span class="match-team">{e["away"]}</span>'
            f'</div>'
        )
    return out


# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════
if "selected_league" not in st.session_state:
    st.session_state.selected_league = "EPL"

SYSTEM_PROMPT = (
    "You are PITCH IQ — an elite football AI analyst with encyclopedic knowledge of world football. "
    "Provide sharp tactical analysis, player breakdowns, club history, head-to-heads, transfer speculation, and formation insights. "
    "Be confident, opinionated, and engaging — like a top pundit blended with a data scientist. "
    "When live standings or scores are provided, reference them precisely. "
    "Format responses with **bold headers** and concise bullet points. Use football emojis sparingly but effectively. "
    f"Current season: {SEASON_LABEL}. Today: {now.strftime('%B %d, %Y')}."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ══════════════════════════════════════════════════════════════
# API KEYS
# ══════════════════════════════════════════════════════════════
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    groq_api_key = None

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    # Brand
    st.markdown(
        '<div class="brand">PITCH<span>IQ</span></div>'
        '<div class="brand-sub">Football Intelligence System</div>',
        unsafe_allow_html=True,
    )

    # League toggle
    st.markdown('<p class="section-hd">▸ League Table</p>', unsafe_allow_html=True)

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
        f'<p style="font-size:10px;color:#2a5a3a;margin:3px 0 8px">'
        f'<span class="live-dot"></span>{sel["flag"]} {sel["name"]} · {SEASON_LABEL}</p>',
        unsafe_allow_html=True,
    )

    with st.spinner(""):
        sdata = espn_standings(sel["espn"])

    st.markdown(standings_html(sdata, sel["rel_start"]), unsafe_allow_html=True)
    st.divider()

    # Top scorers
    st.markdown('<p class="section-hd">▸ Top Scorers</p>', unsafe_allow_html=True)
    with st.spinner(""):
        sc_data = espn_top_scorers(sel["espn"])
    st.markdown(scorers_html(sc_data), unsafe_allow_html=True)
    st.divider()

    # Scores
    st.markdown('<p class="section-hd">▸ Recent Matches</p>', unsafe_allow_html=True)
    with st.spinner(""):
        fixtures = espn_scoreboard(sel["espn"])
    if fixtures:
        st.markdown(scoreboard_html(fixtures), unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:#1a2a3a;font-size:10px;text-align:center">No recent fixtures</p>', unsafe_allow_html=True)

    st.divider()

    # Quick prompts
    st.markdown('<p style="font-size:9px;color:#1a3a2a;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px">Try Asking</p>', unsafe_allow_html=True)
    quick = ["Messi vs Ronaldo GOAT debate", "Best pressing teams 2025", "UCL dark horses", "Haaland vs Kane", "Tiki-taka explained", "Best free kicks ever"]
    cols = st.columns(2)
    for i, q in enumerate(quick):
        with cols[i % 2]:
            st.markdown(f'<span class="pill">{q}</span>', unsafe_allow_html=True)

    st.write("")
    if st.button("⟳  Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()

# ══════════════════════════════════════════════════════════════
# HERO BANNER
# ══════════════════════════════════════════════════════════════
hero_html = f"""
<!DOCTYPE html><html><head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=DM+Sans:wght@300;400;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:transparent;overflow:hidden;height:160px}}
.hero{{
  position:relative;
  background:linear-gradient(135deg,rgba(0,12,24,0.95) 0%,rgba(0,8,18,0.98) 100%);
  border:1px solid rgba(0,255,135,0.12);
  border-radius:16px;padding:20px 26px 18px;
  overflow:hidden;height:160px;
}}
.hero::before{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,#00ff87 30%,#00cfff 70%,transparent);
}}
.hero::after{{
  content:'';position:absolute;
  width:300px;height:300px;border-radius:50%;
  background:radial-gradient(circle,rgba(0,255,135,0.07) 0%,transparent 70%);
  top:-100px;right:-50px;
}}
.title{{
  font-family:'Orbitron',monospace;font-size:38px;font-weight:900;
  letter-spacing:2px;color:#fff;line-height:1;margin-bottom:8px;
}}
.title .hi{{color:#00ff87}}
.title .iq{{
  color:transparent;
  -webkit-text-stroke:1.5px #00ff87;
  text-shadow:0 0 30px rgba(0,255,135,0.4);
}}
.sub{{
  font-size:12px;color:#4a6a82;
  font-family:'DM Sans',sans-serif;font-weight:300;
  letter-spacing:.5px;margin-bottom:14px;
}}
.badges{{display:flex;gap:8px;flex-wrap:wrap;position:relative;z-index:2}}
.badge{{
  display:inline-flex;align-items:center;gap:6px;
  border-radius:5px;padding:4px 12px;
  font-size:10px;font-family:'DM Sans',sans-serif;font-weight:600;
  letter-spacing:.8px;text-transform:uppercase;
}}
.b1{{background:rgba(0,255,135,0.08);border:1px solid rgba(0,255,135,0.25);color:#00ff87}}
.b2{{background:rgba(0,207,255,0.06);border:1px solid rgba(0,207,255,0.18);color:#00cfff}}
.b3{{background:rgba(255,60,110,0.06);border:1px solid rgba(255,60,110,0.18);color:#ff3c6e}}
.dot{{width:5px;height:5px;border-radius:50%;background:#00ff87;animation:p 1.8s ease-in-out infinite}}
@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.2}}}}
.scan{{
  position:absolute;right:30px;top:50%;transform:translateY(-50%);
  width:90px;height:90px;opacity:.15;
}}
.scan circle{{fill:none;stroke:#00ff87;stroke-width:.5}}
.scan line{{stroke:#00ff87;stroke-width:.3}}
</style>
</head><body>
<div class="hero">
  <svg class="scan" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="45"/>
    <circle cx="50" cy="50" r="30"/>
    <circle cx="50" cy="50" r="15"/>
    <line x1="5" y1="50" x2="95" y2="50"/>
    <line x1="50" y1="5" x2="50" y2="95"/>
    <line x1="15" y1="15" x2="85" y2="85"/>
    <line x1="85" y1="15" x2="15" y2="85"/>
  </svg>
  <div class="title"><span class="hi">PITCH</span><span class="iq">IQ</span></div>
  <div class="sub">Live standings &nbsp;·&nbsp; Match scores &nbsp;·&nbsp; Top scorers &nbsp;·&nbsp; Tactical intelligence &nbsp;·&nbsp; Player analytics</div>
  <div class="badges">
    <div class="badge b1"><span class="dot"></span>Live {SEASON_LABEL} via ESPN</div>
    <div class="badge b2">⚡ Groq · Llama 3.1</div>
    <div class="badge b3">∞ No API limits</div>
  </div>
</div>
</body></html>
"""
components.html(hero_html, height=168, scrolling=False)

# ══════════════════════════════════════════════════════════════
# DISPLAY CHAT HISTORY
# ══════════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "🟢" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# ══════════════════════════════════════════════════════════════
# CHAT PIPELINE
# ══════════════════════════════════════════════════════════════
user_input = st.chat_input("Ask anything about football — tactics, players, history, transfers...")

if user_input:
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # ── Build live context ──────────────────────────────────
    live_ctx = ""
    if sdata:
        top5 = sdata[:5]
        lines = [f"{t['rank']}. {t['name']} — {t['pts']}pts ({t['w']}W {t['d']}D {t['l']}L  GD:{t['gd']})" for t in top5]
        live_ctx += f"\n\nLive {sel['name']} Top 5 ({SEASON_LABEL}):\n" + "\n".join(lines)

    if sc_data:
        sc_lines = [f"{i}. {s['name']} ({s['team']}) — {s['goals']} goals" for i, s in enumerate(sc_data, 1)]
        live_ctx += f"\n\n{sel['name']} Top Scorers:\n" + "\n".join(sc_lines)

    if fixtures:
        fx_lines = []
        for e in fixtures:
            if e["state"] in ("in", "post"):
                fx_lines.append(f"{e['home']} {e['hs']}–{e['as_']} {e['away']} ({e['detail']})")
        if fx_lines:
            live_ctx += f"\n\nRecent/Live {sel['name']} Scores:\n" + "\n".join(fx_lines)

    # ── Build prompt ───────────────────────────────────────
    prompt = (
        f"User Question: {user_input}{live_ctx}\n\n"
        "Answer as PITCH IQ — an elite football analyst. "
        "Reference live data naturally if relevant. "
        "Format with **bold headers** and bullet points. Be sharp and insightful."
    )

    st.session_state.messages.append({"role": "user", "content": prompt})

    # ── Call Groq ──────────────────────────────────────────
    with st.chat_message("assistant", avatar="🟢"):
        with st.spinner(""):
            try:
                from groq import Groq
                client = Groq(api_key=groq_api_key)
                resp = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.38,
                    max_tokens=1024,
                )
                reply = resp.choices[0].message.content
            except Exception as e:
                reply = (
                    f"⚠️ **Error connecting to Groq.**\n\n"
                    f"Make sure `GROQ_API_KEY` is set in your Streamlit secrets.\n\n`{e}`"
                )
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})