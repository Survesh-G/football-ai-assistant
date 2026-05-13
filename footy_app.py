"""
PITCH IQ — Football Intelligence System
Fixed: keyboard_double icon | Top scorers ESPN endpoint | Upcoming fixtures | Expand/collapse table
Style: thiswasmajor.com — editorial black, bold contrast, cinematic reveals
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
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# SEASON
# ══════════════════════════════════════════════════════════════════════════════
now = datetime.now()
SEASON       = now.year if now.month >= 7 else now.year - 1
SEASON_LABEL = f"{SEASON}/{str(SEASON + 1)[-2:]}"

# ══════════════════════════════════════════════════════════════════════════════
# ESPN LEAGUE MAP
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
HEADERS   = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}

# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL CSS — MAJOR-INSPIRED: editorial black, bold contrast, cinematic
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Unbounded:wght@400;700;900&family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {
    --ink:    #050505;
    --cream:  #f0ece2;
    --lime:   #c8ff57;
    --red:    #ff2d55;
    --orange: #ff9500;
    --blue:   #3d8bff;
    --muted:  #3a3a3a;
    --border: rgba(248,245,235,0.07);
    --panel:  rgba(8,8,8,0.97);
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width:3px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:var(--lime); border-radius:2px; }

/* ── Root ── */
html, .stApp { background: var(--ink) !important; }
.stApp::before {
    content:''; position:fixed; inset:0; pointer-events:none; z-index:0;
    background:
        radial-gradient(ellipse 120% 50% at 50% -10%, rgba(200,255,87,0.04) 0%, transparent 55%),
        url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M0 0h80v80H0z' fill='none'/%3E%3Cpath d='M0 40h80M40 0v80' stroke='%23ffffff' stroke-opacity='.012' stroke-width='.5'/%3E%3C/svg%3E");
}
header { background:transparent !important; }
.block-container { padding-top:.8rem !important; padding-bottom:3rem !important; position:relative; z-index:1; }

/* ── Global text ── */
*, body, h1,h2,h3,h4,p,div,span,label,li,td,th {
    color: var(--cream) !important;
    font-family: 'Syne', sans-serif !important;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #060606 !important;
    border-right: 1px solid var(--border) !important;
    min-width:295px !important;
}

/* ── Chat messages ── */
.stChatMessage {
    background: #0d0d0d !important;
    border: 1px solid var(--border) !important;
    border-radius:4px !important;
    margin-bottom:8px !important;
}
[data-testid="stChatMessageContent"] p {
    color: var(--cream) !important;
    line-height:1.75 !important;
    font-family:'Syne',sans-serif !important;
}

/* ── Chat input ── */
.stChatInputContainer {
    background: #0d0d0d !important;
    border: 1px solid rgba(200,255,87,0.18) !important;
    border-radius:4px !important;
}
.stChatInputContainer textarea {
    color: var(--cream) !important;
    font-family:'Syne',sans-serif !important;
    font-size:14px !important;
}
.stChatInputContainer textarea::placeholder { color: var(--muted) !important; }

/* ── Radio pills ── */
div[data-testid="stRadio"] > div {
    display:flex !important; gap:4px !important; flex-wrap:wrap !important;
}
div[data-testid="stRadio"] label {
    background: #0d0d0d !important;
    border: 1px solid var(--border) !important;
    border-radius:3px !important; padding:5px 0 !important;
    cursor:pointer !important; font-size:15px !important;
    flex:1 !important; text-align:center !important; transition:all .15s !important;
}
div[data-testid="stRadio"] label:hover { border-color:rgba(200,255,87,.3) !important; }
div[data-testid="stRadio"] label:has(input:checked) {
    background:rgba(200,255,87,.10) !important;
    border-color:var(--lime) !important;
}

/* ── Standings table ── */
.stbl { width:100%; border-collapse:collapse; font-size:10.5px; }
.stbl th {
    color:var(--muted) !important; font-weight:700; padding:5px 3px;
    text-align:center; border-bottom:1px solid var(--border);
    font-size:8.5px; text-transform:uppercase; letter-spacing:1px;
    font-family:'Space Mono',monospace !important;
}
.stbl th:nth-child(2) { text-align:left; }
.stbl td {
    padding:4.5px 3px; text-align:center;
    border-bottom:1px solid rgba(255,255,255,0.022);
    vertical-align:middle; font-size:10.5px;
}
.stbl td:nth-child(2) { text-align:left; }
.stbl tr:hover td { background:rgba(200,255,87,.04); }
.pts  { color:var(--lime)   !important; font-weight:700 !important; font-family:'Space Mono',monospace !important; }
.gdp  { color:var(--lime)   !important; font-family:'Space Mono',monospace !important; }
.gdn  { color:var(--red)    !important; font-family:'Space Mono',monospace !important; }
.rk   { color:var(--muted)  !important; font-family:'Space Mono',monospace !important; font-size:10px !important; }
.rcl  { color:var(--lime)   !important; font-weight:800 !important; }
.rel  { color:var(--orange) !important; font-weight:700 !important; }
.rrel { color:var(--red)    !important; font-weight:700 !important; }

/* ── Scorers ── */
.sctbl { width:100%; border-collapse:collapse; font-size:11px; }
.sctbl td { padding:5px 3px; border-bottom:1px solid rgba(255,255,255,0.03); vertical-align:middle; }
.sc-rank  { color:var(--lime) !important; font-weight:700 !important; font-size:13px !important;
            width:18px; font-family:'Space Mono',monospace !important; }
.sc-goals { color:var(--lime) !important; font-weight:700 !important; font-size:14px !important;
            text-align:right; font-family:'Space Mono',monospace !important; }
.sc-name  { font-weight:700 !important; font-size:11px !important; color:var(--cream) !important; }
.sc-team  { color:var(--muted) !important; font-size:9px !important; }

/* ── Fixture cards ── */
.fix-card {
    border-left:2px solid var(--lime); padding:6px 8px; margin:4px 0;
    background:rgba(200,255,87,0.03);
}
.fix-teams { font-size:11px !important; font-weight:700 !important; color:var(--cream) !important; }
.fix-meta  { font-size:9px !important; color:var(--muted) !important;
             font-family:'Space Mono',monospace !important; margin-top:1px; }
.fix-live  { color:var(--lime) !important; font-size:8px !important;
             font-weight:700 !important; letter-spacing:1.5px; font-family:'Space Mono',monospace !important; }

/* ── Section headers ── */
.section-hd {
    font-size:8.5px !important; font-weight:800 !important;
    color:var(--lime) !important; letter-spacing:3px !important;
    text-transform:uppercase !important; margin:16px 0 8px !important;
    font-family:'Space Mono',monospace !important;
}

/* ── Pills ── */
.pill {
    display:inline-block; border:1px solid var(--border); border-radius:2px;
    padding:3px 8px; font-size:10px !important; color:var(--muted) !important;
    margin:2px; transition:all .2s; font-family:'Syne',sans-serif !important;
}
.pill:hover { border-color:var(--lime) !important; color:var(--lime) !important; }

/* ── Buttons ── */
.stButton > button {
    background:transparent !important; border:1px solid var(--border) !important;
    color:var(--cream) !important; border-radius:3px !important;
    font-family:'Space Mono',monospace !important; font-size:10px !important;
    letter-spacing:1.5px !important; text-transform:uppercase !important;
    transition:all .2s !important; padding:6px 12px !important;
}
.stButton > button:hover {
    border-color:var(--lime) !important; color:var(--lime) !important;
    background:rgba(200,255,87,0.05) !important;
}

hr { border-color:var(--border) !important; margin:12px 0 !important; }

.meta {
    font-size:8.5px !important; color:var(--muted) !important;
    margin-top:8px !important; font-family:'Space Mono',monospace !important; letter-spacing:.5px;
}
.ldot {
    display:inline-block; width:5px; height:5px; background:var(--lime);
    border-radius:50%; animation:lp 1.8s ease-in-out infinite;
    vertical-align:middle; margin-right:5px;
}
@keyframes lp { 0%,100%{opacity:1} 50%{opacity:.15} }

.nodata {
    font-size:9px !important; color:var(--muted) !important;
    font-family:'Space Mono',monospace !important; letter-spacing:1.5px;
    text-align:center; padding:14px 0; border:1px dashed #1a1a1a; border-radius:3px;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ESPN API HELPERS
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_data(ttl=1800, show_spinner=False)
def espn_standings(league_code: str):
    try:
        r = requests.get(f"{ESPN_BASE}/{league_code}/standings", headers=HEADERS, timeout=10)
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


@st.cache_data(ttl=1800, show_spinner=False)
def espn_top_scorers(league_code: str):
    """
    Try multiple ESPN endpoints to get top scorers.
    ESPN doesn't have one universal scorers endpoint, so we try several.
    """
    urls_to_try = [
        f"{ESPN_BASE}/{league_code}/leaders",
        f"https://site.web.api.espn.com/apis/v2/sports/soccer/{league_code}/leaders",
        f"https://sports.core.api.espn.com/v2/sports/soccer/leagues/{league_code}/leaders",
    ]
    for url in urls_to_try:
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code != 200:
                continue
            data = r.json()
            cats = data.get("categories", [])
            for cat in cats:
                cat_name = (cat.get("name", "") + cat.get("displayName", "")).lower()
                if "goal" in cat_name:
                    raw = cat.get("leaders", [])[:5]
                    if not raw:
                        continue
                    out = []
                    for entry in raw:
                        athlete = entry.get("athlete", {})
                        team    = entry.get("team", {})
                        hs      = athlete.get("headshot", {})
                        logos   = team.get("logos", [])
                        out.append({
                            "name":  athlete.get("displayName", "—"),
                            "short": athlete.get("shortName", "—"),
                            "photo": hs.get("href", "") if isinstance(hs, dict) else "",
                            "team":  team.get("shortDisplayName", "—"),
                            "logo":  logos[0].get("href", "") if logos else "",
                            "goals": int(entry.get("value", 0)),
                        })
                    if out:
                        return out
        except Exception:
            continue
    return []


@st.cache_data(ttl=600, show_spinner=False)
def espn_upcoming(league_code: str):
    """Fetch upcoming + live fixtures from ESPN scoreboard."""
    try:
        r = requests.get(f"{ESPN_BASE}/{league_code}/scoreboard", headers=HEADERS, timeout=10)
        r.raise_for_status()
        events = r.json().get("events", [])
        results = []
        for ev in events[:8]:
            comps = ev.get("competitions", [{}])[0]
            comps_teams = comps.get("competitors", [])
            home = next((c for c in comps_teams if c.get("homeAway") == "home"), {})
            away = next((c for c in comps_teams if c.get("homeAway") == "away"), {})
            status  = ev.get("status", {}).get("type", {})
            state   = status.get("state", "pre")
            detail  = status.get("shortDetail", "")
            date_str = ev.get("date", "")
            try:
                dt  = datetime.strptime(date_str[:16], "%Y-%m-%dT%H:%M")
                dts = dt.strftime("%d %b · %H:%M")
            except Exception:
                dts = detail
            results.append({
                "home":   home.get("team", {}).get("shortDisplayName", "?"),
                "away":   away.get("team", {}).get("shortDisplayName", "?"),
                "hs":     home.get("score", ""),
                "as_":    away.get("score", ""),
                "state":  state,
                "detail": detail,
                "date":   dts,
            })
        return results
    except Exception:
        return []


# ══════════════════════════════════════════════════════════════════════════════
# HTML BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

def standings_html(rows, rel_start: int, show_all: bool = False) -> str:
    if not rows:
        return '<div class="nodata">NO DATA · CHECK CONNECTION</div>'
    display = rows if show_all else rows[:5]
    body = ""
    for t in display:
        rank = t["rank"]
        gd   = t["gd"]
        gds  = f"+{gd}" if gd > 0 else str(gd)
        gdc  = "gdp" if gd > 0 else ("gdn" if gd < 0 else "rk")
        rc   = ("rcl"  if rank <= 4
                else "rel"  if rank <= 6
                else "rrel" if rank >= rel_start
                else "rk")
        logo = t["logo"]
        nm   = (t["name"][:13] + "…") if len(t["name"]) > 13 else t["name"]
        body += (
            f"<tr>"
            f'<td class="{rc}">{rank}</td>'
            f'<td>'
            + (f'<img src="{logo}" width="12" height="12" style="vertical-align:middle;margin-right:4px;border-radius:1px;opacity:.85">' if logo else "")
            + f'{nm}</td>'
            f'<td style="font-family:Space Mono,monospace">{t["p"]}</td>'
            f'<td style="font-family:Space Mono,monospace">{t["w"]}</td>'
            f'<td style="font-family:Space Mono,monospace">{t["d"]}</td>'
            f'<td style="font-family:Space Mono,monospace">{t["l"]}</td>'
            f'<td class="{gdc}">{gds}</td>'
            f'<td class="pts">{t["pts"]}</td>'
            f"</tr>"
        )
    ts = now.strftime("%H:%M")
    return (
        '<table class="stbl">'
        '<thead><tr><th>#</th><th>CLUB</th><th>P</th><th>W</th>'
        '<th>D</th><th>L</th><th>GD</th><th>PTS</th></tr></thead>'
        f'<tbody>{body}</tbody></table>'
        f'<p class="meta"><span class="ldot"></span>ESPN FREE · CACHED 30M · {ts}</p>'
        '<p class="meta" style="margin-top:3px">'
        '<span style="color:#c8ff57">▌</span> UCL &nbsp;'
        '<span style="color:#ff9500">▌</span> UEL &nbsp;'
        '<span style="color:#ff2d55">▌</span> REL</p>'
    )


def scorers_html(data) -> str:
    if not data:
        return '<div class="nodata">NOT AVAILABLE FOR THIS LEAGUE</div>'
    rows = ""
    for i, s in enumerate(data, 1):
        photo = s.get("photo", "")
        raw   = s.get("short", "") or s.get("name", "—")
        name  = raw if raw and raw != "—" else s.get("name", "—").split()[-1]
        tm    = s.get("team", "—")
        tm    = (tm[:13] + "…") if len(tm) > 13 else tm
        logo  = s.get("logo", "")
        goals = s.get("goals", 0)
        avatar_img = (
            f'<img src="{photo}" width="26" height="26" '
            f'style="border-radius:50%;vertical-align:middle;margin-right:7px;'
            f'object-fit:cover;border:1px solid rgba(200,255,87,0.15)">'
            if photo else
            f'<span style="display:inline-block;width:26px;height:26px;border-radius:50%;'
            f'background:rgba(200,255,87,0.06);border:1px solid rgba(200,255,87,0.12);'
            f'vertical-align:middle;margin-right:7px;text-align:center;line-height:26px;'
            f'font-size:11px;color:#c8ff57">⚽</span>'
        )
        logo_img = (
            f'<img src="{logo}" width="10" height="10" '
            f'style="vertical-align:middle;margin-right:2px;opacity:.7">'
            if logo else ""
        )
        rows += (
            f'<tr>'
            f'<td class="sc-rank">{i}</td>'
            f'<td>{avatar_img}'
            f'<span class="sc-name">{name}</span><br>'
            f'<span class="sc-team">{logo_img}{tm}</span></td>'
            f'<td class="sc-goals">{goals}</td>'
            f'</tr>'
        )
    return (
        '<table class="sctbl">'
        '<thead><tr>'
        '<th style="font-family:Space Mono,monospace;font-size:8px;color:#3a3a3a;'
        'letter-spacing:1px;padding-bottom:5px;text-align:center">#</th>'
        '<th style="text-align:left;font-family:Space Mono,monospace;font-size:8px;'
        'color:#3a3a3a;letter-spacing:1px;padding-bottom:5px">PLAYER</th>'
        '<th style="font-family:Space Mono,monospace;font-size:8px;color:#c8ff57;'
        'letter-spacing:1px;padding-bottom:5px">⚽</th>'
        '</tr></thead>'
        f'<tbody>{rows}</tbody></table>'
    )


def upcoming_html(events) -> str:
    if not events:
        return '<div class="nodata">NO FIXTURES FOUND</div>'
    out = ""
    for e in events:
        state = e["state"]
        if state == "in":
            badge = f'<span class="fix-live">● LIVE · {e["detail"]}</span>'
            score_mid = (
                f' <span style="color:#c8ff57;font-family:Space Mono,monospace;font-weight:700">'
                f'{e["hs"]} – {e["as_"]}</span> '
            )
        elif state == "post":
            badge = (
                f'<span style="color:#3a3a3a;font-size:8px;'
                f'font-family:Space Mono,monospace;letter-spacing:1px">FT · {e["detail"]}</span>'
            )
            score_mid = (
                f' <span style="color:#c8ff57;font-family:Space Mono,monospace;font-weight:700">'
                f'{e["hs"]} – {e["as_"]}</span> '
            )
        else:
            badge     = (
                f'<span style="color:#3a3a3a;font-size:8px;'
                f'font-family:Space Mono,monospace;letter-spacing:.8px">{e["date"]}</span>'
            )
            score_mid = ' <span style="color:#3a3a3a"> vs </span> '
        out += (
            f'<div class="fix-card">'
            f'{badge}<br>'
            f'<span class="fix-teams">{e["home"]}{score_mid}{e["away"]}</span>'
            f'</div>'
        )
    return out


# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════
if "selected_league"  not in st.session_state: st.session_state.selected_league  = "EPL"
if "table_expanded"   not in st.session_state: st.session_state.table_expanded   = False

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

    # ── Pure SVG logo — zero font/icon dependency ──
    LOGO_SVG = """
    <div style="padding:18px 16px 0;text-align:center">
    <svg width="210" height="70" viewBox="0 0 210 70" fill="none"
         xmlns="http://www.w3.org/2000/svg">
      <!-- Hexagon pitch mark -->
      <polygon points="35,5 56,18 56,44 35,57 14,44 14,18"
               fill="none" stroke="#c8ff57" stroke-width="1.5" opacity=".9"/>
      <!-- Centre lines -->
      <line x1="35" y1="5"  x2="35" y2="57" stroke="#c8ff57" stroke-width=".6" opacity=".3"/>
      <line x1="14" y1="31" x2="56" y2="31" stroke="#c8ff57" stroke-width=".6" opacity=".3"/>
      <line x1="14" y1="18" x2="56" y2="44" stroke="#c8ff57" stroke-width=".4" opacity=".18"/>
      <line x1="56" y1="18" x2="14" y2="44" stroke="#c8ff57" stroke-width=".4" opacity=".18"/>
      <!-- Centre circle -->
      <circle cx="35" cy="31" r="9" fill="none" stroke="#c8ff57" stroke-width=".8" opacity=".35"/>
      <!-- Centre spot -->
      <circle cx="35" cy="31" r="3.5" fill="#c8ff57" opacity=".95"/>
      <!-- Corner arcs hint -->
      <path d="M14 18 Q14 5 35 5" fill="none" stroke="#c8ff57" stroke-width=".3" opacity=".15"/>
      <path d="M56 44 Q56 57 35 57" fill="none" stroke="#c8ff57" stroke-width=".3" opacity=".15"/>
      <!-- PITCH wordmark -->
      <text x="68" y="33" font-family="Arial Black, sans-serif" font-weight="900"
            font-size="23" fill="#f0ece2" letter-spacing=".5">PITCH</text>
      <!-- IQ — lime, outlined feel -->
      <text x="69" y="53" font-family="Arial, sans-serif" font-weight="400"
            font-size="12" fill="#c8ff57" letter-spacing="8">IQ</text>
      <!-- Thin rule between -->
      <line x1="68" y1="37" x2="195" y2="37" stroke="#c8ff57" stroke-width=".4" opacity=".25"/>
    </svg>
    <p style="font-family:monospace;font-size:7.5px;color:#282828;letter-spacing:3.5px;
              text-transform:uppercase;margin:2px 0 16px;text-align:center">
      Football Intelligence
    </p>
    </div>
    """
    st.markdown(LOGO_SVG, unsafe_allow_html=True)

    # ── League radio ──
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
        f'<p style="font-size:9px;color:#2a4020;margin:2px 0 8px;'
        f'font-family:monospace;letter-spacing:1px">'
        f'<span class="ldot"></span>{sel["name"].upper()} · {SEASON_LABEL}</p>',
        unsafe_allow_html=True,
    )

    # Fetch & render standings
    with st.spinner(""):
        sdata = espn_standings(sel["espn"])

    st.markdown(
        standings_html(sdata, sel["rel_start"], st.session_state.table_expanded),
        unsafe_allow_html=True,
    )

    total = len(sdata)
    if total > 5:
        btn_lbl = "▲ COLLAPSE TABLE" if st.session_state.table_expanded else f"▼ SHOW ALL {total} CLUBS"
        if st.button(btn_lbl, use_container_width=True, key="expand_btn"):
            st.session_state.table_expanded = not st.session_state.table_expanded
            st.rerun()

    st.divider()

    # ── Top Scorers ──
    st.markdown('<p class="section-hd">Top Scorers</p>', unsafe_allow_html=True)
    with st.spinner(""):
        sc_data = espn_top_scorers(sel["espn"])
    st.markdown(scorers_html(sc_data), unsafe_allow_html=True)

    st.divider()

    # ── Upcoming Fixtures ──
    st.markdown('<p class="section-hd">Upcoming Fixtures</p>', unsafe_allow_html=True)
    with st.spinner(""):
        fixtures = espn_upcoming(sel["espn"])
    st.markdown(upcoming_html(fixtures), unsafe_allow_html=True)

    st.divider()

    # ── Quick prompts ──
    st.markdown(
        '<p style="font-size:7.5px;color:#282828;letter-spacing:2.5px;'
        'text-transform:uppercase;font-family:monospace;margin-bottom:8px">Try Asking</p>',
        unsafe_allow_html=True,
    )
    for q in ["Messi vs Ronaldo", "Best pressing teams", "UCL dark horses",
              "Haaland analysis", "4-3-3 vs 4-2-3-1"]:
        st.markdown(f'<span class="pill">→ {q}</span>', unsafe_allow_html=True)

    st.write("")
    if st.button("↺  CLEAR CHAT", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# HERO  — editorial cinematic, Major-style
# ══════════════════════════════════════════════════════════════════════════════
hero_html = f"""<!DOCTYPE html><html><head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@400;700;900&family=Space+Mono&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:transparent;overflow:hidden;height:174px}}
.hero{{
  position:relative;height:174px;overflow:hidden;
  background:linear-gradient(135deg,#070707 0%,#040404 100%);
  border:1px solid rgba(248,245,235,0.06);border-radius:6px;
  padding:20px 28px 18px;
}}
/* Sweep scan line */
.hero::before{{
  content:'';position:absolute;top:0;left:-100%;width:55%;height:100%;
  background:linear-gradient(90deg,transparent,rgba(200,255,87,0.035),transparent);
  animation:scan 5s ease-in-out infinite;pointer-events:none;
}}
@keyframes scan{{0%{{left:-55%}}100%{{left:160%}}}}
/* Top lime stripe */
.hero::after{{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,#c8ff57 0%,rgba(200,255,87,.2) 50%,transparent 100%);
}}
.kicker{{
  font-family:'Space Mono',monospace;font-size:8px;
  color:#2e2e2e;letter-spacing:4px;text-transform:uppercase;margin-bottom:9px;
}}
.title{{
  font-family:'Unbounded',sans-serif;font-weight:900;
  font-size:44px;line-height:1;color:#f0ece2;
  margin-bottom:9px;letter-spacing:-1px;
}}
.title .hl{{color:#c8ff57}}
.sub{{
  font-family:'Space Mono',monospace;font-size:9.5px;
  color:#2e2e2e;letter-spacing:.5px;margin-bottom:13px;
}}
.badges{{display:flex;gap:8px;flex-wrap:wrap}}
.badge{{
  display:inline-flex;align-items:center;gap:6px;
  border-radius:2px;padding:3px 10px;
  font-family:'Space Mono',monospace;font-size:8.5px;
  letter-spacing:1px;text-transform:uppercase;
}}
.b1{{border:1px solid rgba(200,255,87,.3);color:#c8ff57;background:rgba(200,255,87,.05)}}
.b2{{border:1px solid rgba(248,245,235,.08);color:#3a3a3a;background:transparent}}
.dot{{width:5px;height:5px;border-radius:50%;background:#c8ff57;
      animation:p 1.8s ease-in-out infinite;display:inline-block}}
@keyframes p{{0%,100%{{opacity:1}}50%{{opacity:.1}}}}
.bg-num{{
  position:absolute;right:20px;bottom:-10px;
  font-family:'Unbounded',sans-serif;font-size:100px;font-weight:900;
  color:rgba(200,255,87,0.03);line-height:1;user-select:none;letter-spacing:-4px;
}}
</style>
</head><body>
<div class="hero">
  <div class="kicker">Football Intelligence System &nbsp;·&nbsp; {SEASON_LABEL}</div>
  <div class="title">PITCH<span class="hl">IQ</span></div>
  <div class="sub">Standings &nbsp;·&nbsp; Top Scorers &nbsp;·&nbsp; Fixtures &nbsp;·&nbsp; Tactics &nbsp;·&nbsp; Player Intel</div>
  <div class="badges">
    <div class="badge b1"><span class="dot"></span>ESPN · No API Limits</div>
    <div class="badge b2">Groq · Llama 3.1</div>
    <div class="badge b2">100% Free</div>
  </div>
  <div class="bg-num">IQ</div>
</div>
</body></html>"""

components.html(hero_html, height=182, scrolling=False)

# ══════════════════════════════════════════════════════════════════════════════
# CHAT HISTORY
# ══════════════════════════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    if msg["role"] != "system":
        # IMPORTANT: Use plain single characters — avoids Material Icon name bug
        avatar = "▶" if msg["role"] == "assistant" else "◆"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# ══════════════════════════════════════════════════════════════════════════════
# CHAT PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
user_input = st.chat_input("Ask anything — tactics, transfers, history, players...")

if user_input:
    with st.chat_message("user", avatar="◆"):
        st.markdown(user_input)

    # Build live context
    live_ctx = ""
    if sdata:
        lines = [
            f"{t['rank']}. {t['name']} — {t['pts']}pts "
            f"({t['w']}W {t['d']}D {t['l']}L GD:{t['gd']})"
            for t in sdata[:5]
        ]
        live_ctx += f"\n\nLive {sel['name']} Top 5 ({SEASON_LABEL}):\n" + "\n".join(lines)
    if sc_data:
        sc_lines = [f"{i}. {s['name']} ({s['team']}) — {s['goals']} goals"
                    for i, s in enumerate(sc_data, 1)]
        live_ctx += f"\n\n{sel['name']} Top Scorers:\n" + "\n".join(sc_lines)
    if fixtures:
        fx = [e for e in fixtures if e["state"] in ("in", "post")]
        if fx:
            live_ctx += f"\n\nRecent {sel['name']} Scores:\n" + "\n".join(
                f"{e['home']} {e['hs']}–{e['as_']} {e['away']}" for e in fx
            )

    prompt = (
        f"User Question: {user_input}{live_ctx}\n\n"
        "Answer as PITCH IQ. Reference live data naturally if relevant. "
        "Bold headers + bullet points. Be sharp, insightful, opinionated."
    )
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="▶"):
        with st.spinner(""):
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
                    "⚠️ **Groq connection error.**\n\n"
                    f"Ensure `GROQ_API_KEY` is set in your Streamlit secrets.\n\n`{e}`"
                )
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})