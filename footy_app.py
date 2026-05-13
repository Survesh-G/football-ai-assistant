import streamlit as st
import requests
from datetime import datetime
import streamlit.components.v1 as components

# ═══════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="PITCH IQ",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# SEASON
# ═══════════════════════════════════════════════════════════════

now = datetime.now()

SEASON = now.year if now.month >= 7 else now.year - 1

SEASON_LABEL = f"{SEASON}/{str(SEASON + 1)[-2:]}"

# ═══════════════════════════════════════════════════════════════
# ESPN CONFIG
# ═══════════════════════════════════════════════════════════════

LEAGUES = {
    "EPL": {
        "name": "Premier League",
        "flag": "🏴",
        "espn": "eng.1",
        "rel_start": 18
    },

    "La Liga": {
        "name": "La Liga",
        "flag": "🇪🇸",
        "espn": "esp.1",
        "rel_start": 18
    },

    "Bundesliga": {
        "name": "Bundesliga",
        "flag": "🇩🇪",
        "espn": "ger.1",
        "rel_start": 16
    },

    "Serie A": {
        "name": "Serie A",
        "flag": "🇮🇹",
        "espn": "ita.1",
        "rel_start": 18
    },

    "Ligue 1": {
        "name": "Ligue 1",
        "flag": "🇫🇷",
        "espn": "fra.1",
        "rel_start": 16
    },

    "UCL": {
        "name": "Champions League",
        "flag": "⭐",
        "espn": "uefa.champions",
        "rel_start": 99
    }
}

ESPN_BASE = "https://site.api.espn.com/apis/v2/sports/soccer"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ═══════════════════════════════════════════════════════════════
# CSS
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

:root {

    --ink:#050505;
    --white:#f5f7fa;
    --cyan:#00e5ff;
    --red:#ff355e;
    --soft:#b8c2cc;
    --panel:#0b0f14;
    --border:rgba(255,255,255,0.08);
}

html, body, [class*="css"]  {

    font-family: 'Inter', sans-serif;
    background-color: var(--ink);
    color: var(--white);
}

.stApp {

    background:
    linear-gradient(
        rgba(0,0,0,0.82),
        rgba(0,0,0,0.82)
    ),

    url("https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=1920&auto=format&fit=crop");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

section[data-testid="stSidebar"] {

    background: rgba(5,5,5,0.96);
    border-right: 1px solid rgba(255,255,255,0.08);
}

h1,h2,h3,h4,p,span,div {

    color: var(--white);
}

.stChatMessage {

    background: rgba(12,12,12,0.92);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 14px;
}

.stChatInputContainer {

    background: rgba(12,12,12,0.95);
    border: 1px solid rgba(0,229,255,0.2);
    border-radius: 14px;
}

.stChatInputContainer textarea {

    color: white;
    font-size: 16px;
}

.stButton > button {

    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.3);
    color: white;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button:hover {

    border-color: #00e5ff;
    color: #00e5ff;
}

.league-header {

    color: #00e5ff;
    font-size: 13px;
    letter-spacing: 2px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 10px;
}

.hero-box {

    background: rgba(10,10,10,0.88);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 35px;
    margin-bottom: 25px;
}

.hero-title {

    font-size: 68px;
    font-weight: 800;
    color: white;
}

.hero-sub {

    font-size: 22px;
    color: #d0d0d0;
    margin-top: 12px;
}

.hero-date {

    margin-top: 15px;
    color: #00e5ff;
    font-size: 15px;
    font-weight: 600;
}

.table {

    width:100%;
    border-collapse: collapse;
}

.table td {

    padding:8px;
    border-bottom:1px solid rgba(255,255,255,0.05);
}

.table tr:hover {

    background: rgba(0,229,255,0.05);
}

.score {

    color:#00e5ff;
    font-weight:700;
}

.soft {

    color:#b8c2cc;
    font-size:13px;
}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# ESPN FUNCTIONS
# ═══════════════════════════════════════════════════════════════

@st.cache_data(ttl=1800)
def espn_standings(league_code):

    try:

        r = requests.get(
            f"{ESPN_BASE}/{league_code}/standings",
            headers=HEADERS,
            timeout=10
        )

        data = r.json()

        groups = data.get("children", []) or [data]

        final = []

        for g in groups:

            standings = g.get("standings", {}).get("entries", [])

            for e in standings:

                team = e.get("team", {})

                stats = {
                    s["name"]: s.get("value", 0)
                    for s in e.get("stats", [])
                }

                final.append({
                    "rank": stats.get("rank", 0),
                    "name": team.get("displayName", ""),
                    "pts": stats.get("points", 0),
                    "gd": stats.get("pointDifferential", 0),
                    "w": stats.get("wins", 0),
                    "d": stats.get("ties", 0),
                    "l": stats.get("losses", 0)
                })

        return final

    except:
        return []

@st.cache_data(ttl=1800)
def espn_top_scorers(league_code):

    urls = [

        f"https://site.api.espn.com/apis/v2/sports/soccer/{league_code}/leaders",

        f"https://site.web.api.espn.com/apis/v2/sports/soccer/{league_code}/leaders"
    ]

    for url in urls:

        try:

            r = requests.get(
                url,
                headers=HEADERS,
                timeout=10
            )

            if r.status_code != 200:
                continue

            data = r.json()

            categories = data.get("categories", [])

            for cat in categories:

                if "goal" in str(cat).lower():

                    leaders = cat.get("leaders", [])

                    output = []

                    for p in leaders[:5]:

                        athlete = p.get("athlete", {})
                        team = p.get("team", {})

                        output.append({

                            "name": athlete.get(
                                "displayName",
                                "Unknown"
                            ),

                            "team": team.get(
                                "displayName",
                                "Unknown"
                            ),

                            "goals": p.get(
                                "value",
                                0
                            )
                        })

                    if output:
                        return output

        except:
            continue

    return []

@st.cache_data(ttl=600)
def espn_upcoming(league_code):

    try:

        r = requests.get(
            f"{ESPN_BASE}/{league_code}/scoreboard",
            headers=HEADERS,
            timeout=10
        )

        data = r.json()

        events = data.get("events", [])

        if not events:
            return []

        final = []

        for ev in events[:6]:

            comp = ev.get("competitions", [{}])[0]

            competitors = comp.get(
                "competitors",
                []
            )

            home = next(
                (
                    c for c in competitors
                    if c.get("homeAway") == "home"
                ),
                {}
            )

            away = next(
                (
                    c for c in competitors
                    if c.get("homeAway") == "away"
                ),
                {}
            )

            final.append({

                "home":
                home.get(
                    "team",
                    {}
                ).get(
                    "shortDisplayName",
                    "?"
                ),

                "away":
                away.get(
                    "team",
                    {}
                ).get(
                    "shortDisplayName",
                    "?"
                ),

                "home_score":
                home.get("score", ""),

                "away_score":
                away.get("score", ""),

                "status":
                ev.get(
                    "status",
                    {}
                ).get(
                    "type",
                    {}
                ).get(
                    "description",
                    ""
                )
            })

        return final

    except:
        return []

# ═══════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content":
            """
            You are PITCH IQ.

            You are an elite football analyst.

            Give:
            - tactical analysis
            - player insights
            - transfers
            - match analysis
            - football intelligence

            Use live data naturally.
            """
        }
    ]

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:

    st.markdown(
        "<h2 style='color:#00e5ff;'>PITCH IQ</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p class='soft'>Football Intelligence System</p>",
        unsafe_allow_html=True
    )

    st.divider()

    selected = st.radio(

        "League",

        list(LEAGUES.keys()),

        horizontal=True,

        label_visibility="collapsed"
    )

    league = LEAGUES[selected]

    standings = espn_standings(
        league["espn"]
    )

    st.markdown(
        f"<p class='league-header'>{league['name']} TABLE</p>",
        unsafe_allow_html=True
    )

    if standings:

        html = "<table class='table'>"

        for team in standings[:5]:

            html += f"""
            <tr>
                <td>{team['rank']}</td>
                <td>{team['name']}</td>
                <td class='score'>{team['pts']}</td>
            </tr>
            """

        html += "</table>"

        st.markdown(
            html,
            unsafe_allow_html=True
        )

    st.divider()

    scorers = espn_top_scorers(
        league["espn"]
    )

    st.markdown(
        "<p class='league-header'>TOP SCORERS</p>",
        unsafe_allow_html=True
    )

    if scorers:

        for s in scorers:

            st.markdown(
                f"""
                <div style='margin-bottom:12px'>
                <b>{s['name']}</b><br>
                <span class='soft'>
                {s['team']} · ⚽ {s['goals']}
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            "<p class='soft'>No scorer data available</p>",
            unsafe_allow_html=True
        )

    st.divider()

    fixtures = espn_upcoming(
        league["espn"]
    )

    st.markdown(
        "<p class='league-header'>UPCOMING FIXTURES</p>",
        unsafe_allow_html=True
    )

    if fixtures:

        for f in fixtures:

            st.markdown(
                f"""
                <div style='margin-bottom:16px'>
                <b>{f['home']} vs {f['away']}</b><br>
                <span class='soft'>
                {f['status']}
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            "<p class='soft'>No fixture data available</p>",
            unsafe_allow_html=True
        )

    st.divider()

    quick_prompts = [

        "Messi vs Ronaldo",

        "Best pressing teams",

        "Haaland analysis",

        "Real Madrid tactics",

        "Best young midfielders"
    ]

    for q in quick_prompts:

        if st.button(
            q,
            use_container_width=True
        ):
            st.session_state.prefill = q

# ═══════════════════════════════════════════════════════════════
# HERO SECTION
# ═══════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="hero-box">

<div class="hero-title">
PITCH IQ
</div>

<div class="hero-sub">
Elite football intelligence, tactical analysis, player scouting, and live football insights.
</div>

<div class="hero-date">
Live football data updated till: {SEASON_LABEL} season
</div>

</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CHAT HISTORY
# ═══════════════════════════════════════════════════════════════

for msg in st.session_state.messages:

    if msg["role"] != "system":

        with st.chat_message(msg["role"]):

            st.markdown(msg["content"])

# ═══════════════════════════════════════════════════════════════
# GROQ
# ═══════════════════════════════════════════════════════════════

try:

    from groq import Groq

    groq_api_key = st.secrets["GROQ_API_KEY"]

    client = Groq(api_key=groq_api_key)

except:

    client = None

# ═══════════════════════════════════════════════════════════════
# CHAT INPUT
# ═══════════════════════════════════════════════════════════════

default_prompt = st.session_state.get(
    "prefill",
    ""
)

user_input = st.chat_input(
    "Ask anything about football..."
)

if user_input:

    with st.chat_message("user"):

        st.markdown(user_input)

    st.session_state.messages.append({

        "role": "user",

        "content": user_input
    })

    live_context = ""

    if standings:

        live_context += (
            f"\n\nCurrent {league['name']} standings:\n"
        )

        for t in standings[:5]:

            live_context += (
                f"{t['rank']}. "
                f"{t['name']} "
                f"- {t['pts']} pts\n"
            )

    if scorers:

        live_context += (
            f"\nTop scorers:\n"
        )

        for s in scorers:

            live_context += (
                f"{s['name']} "
                f"({s['team']}) "
                f"- {s['goals']} goals\n"
            )

    final_prompt = f"""
    User Question:
    {user_input}

    Live Football Data:
    {live_context}

    Answer like an elite football analyst.
    """

    with st.chat_message("assistant"):

        with st.spinner("Analyzing..."):

            try:

                response = client.chat.completions.create(

                    model="llama-3.1-8b-instant",

                    messages=[
                        {
                            "role": "user",
                            "content": final_prompt
                        }
                    ],

                    temperature=0.4,

                    max_tokens=900
                )

                reply = response.choices[0].message.content

            except Exception as e:

                reply = f"""
                Error connecting to Groq API.

                {e}
                """

        st.markdown(reply)

    st.session_state.messages.append({

        "role": "assistant",

        "content": reply
    })