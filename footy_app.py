import streamlit as st
import requests
from datetime import datetime

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
# DATE + SEASON
# ═══════════════════════════════════════════════════════════════

now = datetime.now()

SEASON = now.year if now.month >= 7 else now.year - 1
SEASON_LABEL = f"{SEASON}/{str(SEASON + 1)[-2:]}"

# ═══════════════════════════════════════════════════════════════
# GROQ
# ═══════════════════════════════════════════════════════════════

from groq import Groq

client = Groq(
    api_key=st.secrets["GROQ_API_KEY"]
)

# ═══════════════════════════════════════════════════════════════
# ESPN CONFIG
# ═══════════════════════════════════════════════════════════════

LEAGUES = {

    "EPL": {
        "name": "Premier League",
        "espn": "eng.1"
    },

    "La Liga": {
        "name": "La Liga",
        "espn": "esp.1"
    },

    "Bundesliga": {
        "name": "Bundesliga",
        "espn": "ger.1"
    },

    "Serie A": {
        "name": "Serie A",
        "espn": "ita.1"
    },

    "Ligue 1": {
        "name": "Ligue 1",
        "espn": "fra.1"
    },

    "UCL": {
        "name": "Champions League",
        "espn": "uefa.champions"
    }
}

ESPN_BASE = "https://site.api.espn.com/apis/v2/sports/soccer"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {

    font-family: 'Inter', sans-serif;
}

.stApp {

    background:
    linear-gradient(
        rgba(0,0,0,0.84),
        rgba(0,0,0,0.88)
    ),

    url("https://images.unsplash.com/photo-1518091043644-c1d4457512c6?q=80&w=1974&auto=format&fit=crop");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

section[data-testid="stSidebar"] {

    background: rgba(5,5,5,0.96);
    border-right: 1px solid rgba(255,255,255,0.08);
}

h1,h2,h3,h4,p,span,div,label {

    color: white !important;
}

.stChatMessage {

    background: rgba(10,10,10,0.82);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 15px;
    margin-bottom: 14px;
}

.stChatInputContainer {

    background: rgba(10,10,10,0.92);
    border: 1px solid rgba(0,229,255,0.2);
    border-radius: 14px;
}

.stButton > button {

    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.28);
    color: white;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button:hover {

    border-color: #00e5ff;
    color: #00e5ff;
}

.hero {

    background: rgba(10,10,10,0.82);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 35px;
    margin-bottom: 25px;
}

.hero-title {

    font-size: 72px;
    font-weight: 800;
    color: white;
}

.hero-sub {

    font-size: 24px;
    color: #d1d1d1;
    margin-top: 12px;
}

.hero-date {

    margin-top: 15px;
    color: #00e5ff;
    font-size: 16px;
    font-weight: 600;
}

.table {

    width: 100%;
    border-collapse: collapse;
}

.table td {

    padding: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}

.table tr:hover {

    background: rgba(0,229,255,0.06);
}

.score {

    color: #00e5ff;
    font-weight: 700;
}

.soft {

    color: #b8c2cc !important;
    font-size: 13px;
}

.material-icons,
.material-icons-outlined,
.material-icons-round,
.material-symbols-outlined,
.material-symbols-rounded,
[class*="material-icon"],
[class*="material-symbol"] {

    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
    overflow: hidden !important;
}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# ESPN FUNCTIONS
# ═══════════════════════════════════════════════════════════════

@st.cache_data(ttl=1800)
def get_standings(league_code):

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

            standings = g.get(
                "standings",
                {}
            ).get(
                "entries",
                []
            )

            for e in standings:

                team = e.get("team", {})

                stats = {
                    s["name"]: s.get("value", 0)
                    for s in e.get("stats", [])
                }

                final.append({

                    "rank": stats.get("rank", 0),

                    "name": team.get(
                        "displayName",
                        ""
                    ),

                    "pts": stats.get("points", 0)
                })

        return final

    except:
        return []

@st.cache_data(ttl=1800)
def get_top_scorers(league_code):

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

            categories = data.get(
                "categories",
                []
            )

            for cat in categories:

                if "goal" in str(cat).lower():

                    leaders = cat.get(
                        "leaders",
                        []
                    )

                    output = []

                    for p in leaders[:5]:

                        athlete = p.get(
                            "athlete",
                            {}
                        )

                        team = p.get(
                            "team",
                            {}
                        )

                        output.append({

                            "name":
                            athlete.get(
                                "displayName",
                                "Unknown"
                            ),

                            "team":
                            team.get(
                                "displayName",
                                "Unknown"
                            ),

                            "goals":
                            p.get(
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
def get_fixtures(league_code):

    try:

        r = requests.get(
            f"{ESPN_BASE}/{league_code}/scoreboard",
            headers=HEADERS,
            timeout=10
        )

        data = r.json()

        events = data.get(
            "events",
            []
        )

        final = []

        for ev in events[:5]:

            comp = ev.get(
                "competitions",
                [{}]
            )[0]

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

            Elite football intelligence system.

            Provide:
            - tactical analysis
            - player analysis
            - football insights
            - club analysis
            - transfer analysis
            """
        }
    ]

# ═══════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════

with st.sidebar:

    st.markdown(
        "<h1 style='color:#00e5ff;'>PITCH IQ</h1>",
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

    standings = get_standings(
        league["espn"]
    )

    st.markdown(
        f"### {league['name']} Table"
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

    scorers = get_top_scorers(
        league["espn"]
    )

    st.markdown("### Top Scorers")

    if scorers:

        for s in scorers:

            st.markdown(
                f"""
                <b>{s['name']}</b><br>
                <span class='soft'>
                {s['team']} · ⚽ {s['goals']}
                </span>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            "<p class='soft'>No scorer data available</p>",
            unsafe_allow_html=True
        )

    st.divider()

    fixtures = get_fixtures(
        league["espn"]
    )

    st.markdown("### Upcoming Fixtures")

    if fixtures:

        for f in fixtures:

            st.markdown(
                f"""
                <b>{f['home']} vs {f['away']}</b><br>
                <span class='soft'>
                {f['status']}
                </span>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            "<p class='soft'>No fixtures available</p>",
            unsafe_allow_html=True
        )

    st.divider()

    quick_prompts = [

        "Messi vs Ronaldo",

        "Best pressing teams",

        "Real Madrid tactics",

        "Haaland analysis",

        "Best young midfielders"
    ]

    for q in quick_prompts:

        if st.button(
            q,
            use_container_width=True
        ):
            st.session_state.prefill = q

# ═══════════════════════════════════════════════════════════════
# HERO
# ═══════════════════════════════════════════════════════════════

st.markdown(f"""
<div class="hero">

<div class="hero-title">
⚽ PITCH IQ
</div>

<div class="hero-sub">
Elite football intelligence,
tactical analysis,
live standings,
player scouting,
and football insights.
</div>

<div class="hero-date">
📅 Live football data updated till:
{SEASON_LABEL} season
</div>

</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# CHAT HISTORY
# ═══════════════════════════════════════════════════════════════

for msg in st.session_state.messages:

    if msg["role"] != "system":

        role = msg.get(
            "role",
            "assistant"
        )

        content = msg.get(
            "content",
            ""
        )

        content = content.replace(
            "keyboard_double_arrow_right",
            ""
        )

        with st.chat_message(role):

            st.markdown(content)

# ═══════════════════════════════════════════════════════════════
# CHAT INPUT
# ═══════════════════════════════════════════════════════════════

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
            f"\nCurrent {league['name']} standings:\n"
        )

        for t in standings[:5]:

            live_context += (
                f"{t['rank']}. "
                f"{t['name']} "
                f"- {t['pts']} pts\n"
            )

    if scorers:

        live_context += (
            "\nTop scorers:\n"
        )

        for s in scorers:

            live_context += (
                f"{s['name']} "
                f"({s['team']}) "
                f"- {s['goals']} goals\n"
            )

    prompt = f"""
    User Question:
    {user_input}

    Live Football Data:
    {live_context}

    Answer like an elite football analyst.
    """

    with st.chat_message("assistant"):

        with st.spinner("Analyzing football intelligence..."):

            try:

                response = client.chat.completions.create(

                    model="llama-3.1-8b-instant",

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.4,

                    max_tokens=900
                )

                reply = (
                    response
                    .choices[0]
                    .message
                    .content
                )

            except Exception as e:

                reply = f"""
                Error connecting to Groq API.

                {e}
                """

        reply = reply.replace(
            "keyboard_double_arrow_right",
            ""
        )

        st.markdown(reply)

    st.session_state.messages.append({

        "role": "assistant",

        "content": reply
    })