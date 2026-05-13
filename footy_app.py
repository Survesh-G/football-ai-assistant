import streamlit as st
from groq import Groq
import requests
from datetime import datetime
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(page_title="Football AI Assistant", page_icon="⚽", layout="wide")

# ══════════════════════════════════════════════════════════════
# LEAGUE CONFIG  (API-Football league IDs)
# ══════════════════════════════════════════════════════════════
LEAGUES = {
    "EPL":        {"name": "Premier League", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "id": 39,  "teams": 20, "rel_start": 18},
    "La Liga":    {"name": "La Liga",         "flag": "🇪🇸",       "id": 140, "teams": 20, "rel_start": 18},
    "Bundesliga": {"name": "Bundesliga",      "flag": "🇩🇪",       "id": 78,  "teams": 18, "rel_start": 16},
    "Serie A":    {"name": "Serie A",         "flag": "🇮🇹",       "id": 135, "teams": 20, "rel_start": 18},
    "Ligue 1":    {"name": "Ligue 1",         "flag": "🇫🇷",       "id": 61,  "teams": 18, "rel_start": 16},
}

# ══════════════════════════════════════════════════════════════
# CURRENT SEASON
# ══════════════════════════════════════════════════════════════
now = datetime.now()
SEASON = now.year if now.month >= 7 else now.year - 1
SEASON_LABEL = f"{SEASON}/{str(SEASON + 1)[-2:]}"

# ══════════════════════════════════════════════════════════════
# GLOBAL CSS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap');

/* Background */
.stApp {
    background-image: linear-gradient(rgba(0,0,0,0.86),rgba(0,0,0,0.93)),
        url("https://images.unsplash.com/photo-1518091043644-c1d4457512c6?q=80&w=2070&auto=format&fit=crop");
    background-size:cover; background-position:center; background-attachment:fixed;
}
header { background:transparent !important; }
.block-container { padding-top:1.2rem !important; }

/* Global text */
body,h1,h2,h3,h4,h5,h6,p,div,span,label,li,td,th {
    color:#fff !important; font-family:'Inter',sans-serif !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background:linear-gradient(160deg,rgba(6,6,6,0.98),rgba(14,14,14,0.98)) !important;
    border-right:1px solid rgba(255,255,255,0.06) !important;
    min-width:320px !important;
}

/* Chat */
.stChatMessage {
    background-color:rgba(20,20,20,0.75) !important;
    border:1px solid rgba(255,255,255,0.07) !important;
    border-radius:16px !important; backdrop-filter:blur(12px) !important;
}
.stChatInputContainer {
    background:rgba(12,12,12,0.88) !important; border-radius:14px !important;
    border:1px solid rgba(255,255,255,0.09) !important; backdrop-filter:blur(10px) !important;
}
.stChatInputContainer textarea { color:white !important; }

/* ── League radio as pill toggle ── */
div[data-testid="stRadio"] { margin-bottom:6px; }
div[data-testid="stRadio"] > div {
    display:flex !important; gap:5px !important; flex-wrap:nowrap !important;
}
div[data-testid="stRadio"] label {
    background:rgba(255,255,255,0.05) !important;
    border:1px solid rgba(255,255,255,0.10) !important;
    border-radius:8px !important; padding:5px 0 !important;
    cursor:pointer !important; font-size:17px !important;
    flex:1 !important; text-align:center !important;
    transition:all .18s ease !important;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background:rgba(74,222,128,0.18) !important;
    border-color:#4ade80 !important;
    box-shadow:0 0 8px rgba(74,222,128,0.25) !important;
}

/* ── Standings table ── */
.stbl { width:100%; border-collapse:collapse; font-size:10.5px; }
.stbl th {
    color:#666 !important; font-weight:500; padding:3px 3px;
    text-align:center; border-bottom:1px solid rgba(255,255,255,0.10);
    font-size:9.5px; text-transform:uppercase; letter-spacing:.4px;
}
.stbl th:nth-child(2) { text-align:left; }
.stbl td { padding:3.5px 3px; text-align:center; border-bottom:1px solid rgba(255,255,255,0.03); vertical-align:middle; }
.stbl td:nth-child(2) { text-align:left; }
.stbl tr:hover td { background:rgba(255,255,255,0.03); }
.pts  { font-weight:700 !important; }
.gdp  { color:#4ade80 !important; }
.gdn  { color:#f87171 !important; }
.rcl  { color:#4ade80 !important; font-weight:700 !important; }
.rel  { color:#fb923c !important; font-weight:600 !important; }
.rrel { color:#f87171 !important; font-weight:600 !important; }

/* ── Scorers table ── */
.sctbl { width:100%; border-collapse:collapse; font-size:11px; }
.sctbl td { padding:5px 3px; border-bottom:1px solid rgba(255,255,255,0.04); vertical-align:middle; }
.sc-rank  { color:#4ade80 !important; font-weight:700 !important; font-size:14px !important; width:18px; }
.sc-goals { color:#4ade80 !important; font-weight:700 !important; font-size:15px !important; text-align:right; }

/* Floating football */
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-8px)} }
.fb-icon { animation:float 3s ease-in-out infinite; font-size:50px; text-align:center; display:block; margin:4px auto 0; }

/* Pills */
.pill { display:inline-block; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.11);
    border-radius:999px; padding:2px 9px; font-size:11px !important; color:#bbb !important; margin:2px; }

/* Buttons */
.stButton > button {
    background:rgba(255,255,255,0.04) !important; border:1px solid rgba(255,255,255,0.13) !important;
    color:white !important; border-radius:10px !important; transition:all .2s !important;
}
.stButton > button:hover { background:rgba(255,255,255,0.10) !important; }
hr { border-color:rgba(255,255,255,0.07) !important; }
.meta { font-size:9.5px !important; color:#444 !important; margin-top:5px !important; }
.section-hd { font-size:11px !important; font-weight:600 !important; color:#888 !important;
    letter-spacing:.8px !important; text-transform:uppercase !important; margin-bottom:6px !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# API KEYS & CLIENTS
# ══════════════════════════════════════════════════════════════
groq_api_key     = st.secrets["GROQ_API_KEY"]
football_api_key = st.secrets["FOOTBALL_API_KEY"]
client           = Groq(api_key=groq_api_key)


# ══════════════════════════════════════════════════════════════
# CACHED API HELPERS
# ttl=1800 → refresh every 30 minutes
# api_key passed as arg so cache key includes it (multi-user safe)
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=1800, show_spinner=False)
def fetch_standings(league_id: int, season: int, api_key: str):
    try:
        r = requests.get(
            "https://v3.football.api-sports.io/standings",
            params={"league": league_id, "season": season},
            headers={"x-apisports-key": api_key},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        if data.get("response"):
            return data["response"][0]["league"]["standings"][0]
    except Exception:
        pass
    return []


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_top_scorers(league_id: int, season: int, api_key: str):
    try:
        r = requests.get(
            "https://v3.football.api-sports.io/players/topscorers",
            params={"league": league_id, "season": season},
            headers={"x-apisports-key": api_key},
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        return data.get("response", [])[:5]
    except Exception:
        pass
    return []


@st.cache_data(ttl=1800, show_spinner=False)
def fetch_player_data(query: str, season: int, api_key: str):
    try:
        r = requests.get(
            "https://v3.football.api-sports.io/players",
            params={"search": query, "season": season},
            headers={"x-apisports-key": api_key},
            timeout=10,
        )
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}


# ══════════════════════════════════════════════════════════════
# HTML BUILDERS  (compact, single-line tags → no parser issues)
# ══════════════════════════════════════════════════════════════
def standings_html(rows_data, rel_start: int) -> str:
    if not rows_data:
        return '<p style="color:#555;font-size:11px;padding:8px 0">Data unavailable — check API quota</p>'

    rows = ""
    for t in rows_data:
        rank = t["rank"]
        name = t["team"]["name"]
        logo = t["team"]["logo"]
        p    = t["all"]["played"]
        w    = t["all"]["win"]
        d    = t["all"]["draw"]
        l    = t["all"]["lose"]
        gd   = t["goalsDiff"]
        pts  = t["points"]

        nm   = (name[:14] + "…") if len(name) > 14 else name
        gdc  = "gdp" if gd > 0 else ("gdn" if gd < 0 else "")
        gds  = f"+{gd}" if gd > 0 else str(gd)
        rc   = "rcl" if rank <= 4 else ("rel" if rank <= 6 else ("rrel" if rank >= rel_start else ""))

        rows += (
            f'<tr>'
            f'<td class="{rc}">{rank}</td>'
            f'<td><img src="{logo}" width="13" height="13" style="vertical-align:middle;margin-right:3px;border-radius:2px">{nm}</td>'
            f'<td>{p}</td><td>{w}</td><td>{d}</td><td>{l}</td>'
            f'<td class="{gdc}">{gds}</td>'
            f'<td class="pts">{pts}</td>'
            f'</tr>'
        )

    ts = now.strftime("%H:%M")
    return (
        '<table class="stbl">'
        '<thead><tr>'
        '<th>#</th><th>Club</th><th>P</th><th>W</th><th>D</th><th>L</th><th>GD</th><th>Pts</th>'
        '</tr></thead>'
        f'<tbody>{rows}</tbody>'
        '</table>'
        f'<p class="meta">🟢 cached · refreshes every 30 min · {ts}</p>'
        '<p class="meta">'
        '<span style="color:#4ade80">■</span> UCL &nbsp;'
        '<span style="color:#fb923c">■</span> UEL &nbsp;'
        '<span style="color:#f87171">■</span> Relegation'
        '</p>'
    )


def scorers_html(scorers_data) -> str:
    if not scorers_data:
        return '<p style="color:#555;font-size:11px;padding:8px 0">Data unavailable — check API quota</p>'

    rows = ""
    for i, s in enumerate(scorers_data, 1):
        player    = s["player"]
        stats     = s["statistics"][0]
        full_name = player["name"]
        photo     = player.get("photo", "")
        team_name = stats["team"]["name"]
        team_logo = stats["team"].get("logo", "")
        goals     = stats["goals"]["total"] or 0
        assists   = stats["goals"].get("assists") or 0

        # Display last name for space efficiency
        display = full_name.split(" ")[-1] if " " in full_name else full_name
        tm_short = (team_name[:13] + "…") if len(team_name) > 13 else team_name

        rows += (
            f'<tr>'
            f'<td class="sc-rank">{i}</td>'
            f'<td>'
            f'<img src="{photo}" width="24" height="24" style="border-radius:50%;vertical-align:middle;margin-right:6px;object-fit:cover">'
            f'<span style="font-weight:600">{display}</span>'
            f'<br>'
            f'<span style="color:#666;font-size:9.5px">'
            f'<img src="{team_logo}" width="11" height="11" style="vertical-align:middle;margin-right:2px">{tm_short}'
            f'</span>'
            f'</td>'
            f'<td class="sc-goals">{goals}⚽ <span style="color:#888;font-size:10px">{assists}🅰️</span></td>'
            f'</tr>'
        )

    return f'<table class="sctbl"><tbody>{rows}</tbody></table>'


# ══════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════
if "selected_league" not in st.session_state:
    st.session_state.selected_league = "EPL"

SYSTEM_PROMPT = (
    "You are an elite football AI analyst with deep expertise across world football. "
    "Provide sharp tactical analysis, player breakdowns, club history, head-to-heads, and insights. "
    "Be confident, opinionated, and engaging — like a top pundit. "
    "When live standings context is provided, reference it naturally. "
    "Format responses with **bold headers** and concise bullet points. "
    f"Current season: {SEASON_LABEL}."
)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]


# ══════════════════════════════════════════════════════════════
# SIDEBAR — league table + top scorers
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<span class="fb-icon">⚽</span>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align:center;font-family:\'Bebas Neue\',sans-serif;'
        'font-size:24px;letter-spacing:3px;margin:2px 0 14px">Football AI</p>',
        unsafe_allow_html=True,
    )

    # ── League toggle ──────────────────────────────────────
    st.markdown('<p class="section-hd">📊 League Table</p>', unsafe_allow_html=True)

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
        f'<p style="font-size:11px;color:#4ade80;margin:3px 0 8px">'
        f'{sel["flag"]} {sel["name"]} · {SEASON_LABEL}</p>',
        unsafe_allow_html=True,
    )

    # ── Fetch + render standings ───────────────────────────
    with st.spinner(""):
        sdata = fetch_standings(sel["id"], SEASON, football_api_key)

    st.markdown(standings_html(sdata, sel["rel_start"]), unsafe_allow_html=True)

    st.divider()

    # ── Top scorers ────────────────────────────────────────
    st.markdown('<p class="section-hd">🥇 Top Scorers</p>', unsafe_allow_html=True)

    with st.spinner(""):
        sc_data = fetch_top_scorers(sel["id"], SEASON, football_api_key)

    st.markdown(scorers_html(sc_data), unsafe_allow_html=True)

    st.divider()

    # ── Quick prompts ──────────────────────────────────────
    st.markdown('<p style="font-size:10px;color:#444;margin-bottom:5px">💬 Try asking:</p>', unsafe_allow_html=True)
    for q in ["Messi vs Ronaldo", "Guardiola tactics", "Last El Clasico", "Arsenal form"]:
        st.markdown(f'<span class="pill">• {q}</span>', unsafe_allow_html=True)

    st.write("")
    if st.button("🗑️  Clear Chat", use_container_width=True):
        st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        st.rerun()


# ══════════════════════════════════════════════════════════════
# HERO  (components.html → immune to markdown parser)
# ══════════════════════════════════════════════════════════════
hero = f"""<!DOCTYPE html>
<html><head>
<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{background:transparent;overflow:hidden}}
  .hero{{background:rgba(10,10,10,0.70);padding:24px 28px 20px;border-radius:18px;border:1px solid rgba(255,255,255,0.07);backdrop-filter:blur(14px)}}
  .title{{font-family:'Bebas Neue',sans-serif;font-size:56px;letter-spacing:2px;color:#fff;line-height:1;margin-bottom:8px}}
  .g{{color:#4ade80}}
  .sub{{font-size:14px;color:#bbb;font-family:'Inter',sans-serif;font-weight:300;line-height:1.55;margin-bottom:12px}}
  .badges{{display:flex;gap:8px;flex-wrap:wrap}}
  .badge{{display:inline-flex;align-items:center;gap:5px;background:rgba(74,222,128,0.10);border:1px solid rgba(74,222,128,0.28);border-radius:999px;padding:4px 12px;font-size:11px;color:#4ade80;font-family:'Inter',sans-serif;font-weight:500}}
  .badge2{{background:rgba(255,255,255,0.06);border-color:rgba(255,255,255,0.15);color:#aaa}}
  .dot{{width:6px;height:6px;border-radius:50%;background:#4ade80;animation:pulse 1.8s ease-in-out infinite}}
  @keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.3;transform:scale(.65)}}}}
</style>
</head><body>
<div class="hero">
  <div class="title">&#9917; Football <span class="g">AI</span> Assistant</div>
  <div class="sub">Live standings &middot; Top scorers &middot; Tactical breakdowns &middot; Player intelligence &middot; Match analysis</div>
  <div class="badges">
    <div class="badge"><span class="dot"></span>Live {SEASON_LABEL} data</div>
    <div class="badge badge2">⚡ Groq + Llama 3.1</div>
    <div class="badge badge2">📊 API-Football</div>
  </div>
</div>
</body></html>"""

components.html(hero, height=182, scrolling=False)


# ══════════════════════════════════════════════════════════════
# DISPLAY CHAT HISTORY
# ══════════════════════════════════════════════════════════════
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


# ══════════════════════════════════════════════════════════════
# CHAT INPUT + PIPELINE
# ══════════════════════════════════════════════════════════════
user_input = st.chat_input("Ask anything about football...")

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    # ── Inject live standings as context ──────────────────
    live_ctx = ""
    if sdata:
        top5 = sdata[:5]
        lines = [
            f"{t['rank']}. {t['team']['name']} — {t['points']}pts "
            f"({t['all']['win']}W {t['all']['draw']}D {t['all']['lose']}L  GD:{t['goalsDiff']})"
            for t in top5
        ]
        live_ctx = f"\n\nLive {sel['name']} Top 5 ({SEASON_LABEL}):\n" + "\n".join(lines)

    if sc_data:
        sc_lines = [
            f"{i}. {s['player']['name']} ({s['statistics'][0]['team']['name']}) "
            f"— {s['statistics'][0]['goals']['total']} goals"
            for i, s in enumerate(sc_data, 1)
        ]
        live_ctx += f"\n\n{sel['name']} Top Scorers:\n" + "\n".join(sc_lines)

    # ── Player-specific API lookup ─────────────────────────
    player_data = fetch_player_data(user_input, SEASON, football_api_key)
    api_has_data = (
        isinstance(player_data.get("response"), list)
        and len(player_data["response"]) > 0
    )

    # ── Build prompt ───────────────────────────────────────
    if api_has_data:
        prompt = (
            f"User Question: {user_input}\n\n"
            f"Live Player Data:\n{player_data}{live_ctx}\n\n"
            "Use this data naturally. Include overview, key stats, tactical analysis, insights. "
            "Format with **bold headers** and bullet points."
        )
    else:
        prompt = (
            f"User Question: {user_input}{live_ctx}\n\n"
            "Answer as an elite football analyst using your deep knowledge. "
            "Do NOT mention missing data or API issues. "
            "Include overview, highlights, tactical analysis, insights. "
            "Format with **bold headers** and bullet points."
        )

    st.session_state.messages.append({"role": "user", "content": prompt})

    # ── Generate response ──────────────────────────────────
    with st.chat_message("assistant"):
        with st.spinner("⚽ Analysing..."):
            try:
                resp = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.35,
                    max_tokens=1024,
                )
                reply = resp.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ Error generating response: {e}"

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})