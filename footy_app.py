import streamlit as st
import requests
from datetime import datetime
import streamlit.components.v1 as components

# ══════════════════════════════════════════════════════════════════════════════
# 1. PAGE CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PITCH IQ · Football Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# 2. THE GHOST FIX: JAVASCRIPT DOM PURGE
# This loop kills the Material Icons stylesheet that causes the ghost text.
# ══════════════════════════════════════════════════════════════════════════════
components.html(
    """
    <script>
    const nukeIcons = () => {
        const links = window.parent.document.getElementsByTagName('link');
        for (let i = 0; i < links.length; i++) {
            if (links[i].href.includes('fonts.googleapis.com/icon') || 
                links[i].href.includes('Material+Icons')) {
                links[i].remove();
            }
        }
        const styles = window.parent.document.getElementsByTagName('style');
        for (let i = 0; i < styles.length; i++) {
            if (styles[i].innerText.includes('Material Icons')) {
                styles[i].remove();
            }
        }
    };
    nukeIcons();
    setInterval(nukeIcons, 500); 
    </script>
    """,
    height=0,
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. GLOBAL STYLING (PITCH IQ THEME)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --ink: #05080f; --white: #f4f6fb; --cyan: #00d4ff; --red: #ff3154; --muted: #4a5568;
}

html, .stApp { background: var(--ink) !important; }
*, body, p, div, span, label { color: var(--white) !important; font-family: 'Inter', sans-serif !important; }

/* Hide standard avatars to prevent font fallback issues */
[data-testid="stChatMessage"] > div:first-child { display: none !important; }

.stChatMessage {
    background: rgba(10, 14, 26, 0.7) !important;
    border: 1px solid rgba(244, 246, 251, 0.05) !important;
    border-radius: 4px !important;
    margin-bottom: 12px !important;
    padding: 1.2rem !important;
}

section[data-testid="stSidebar"] { 
    background: #070b16 !important; 
    border-right: 1px solid rgba(0,212,255,0.1) !important; 
}

.stbl { width: 100%; border-collapse: collapse; font-size: 11px; margin-top: 10px; }
.stbl th { color: var(--muted) !important; font-family: 'JetBrains Mono'; border-bottom: 1px solid rgba(0,212,255,0.1); padding: 5px; text-align: left; }
.stbl td { padding: 5px; border-bottom: 1px solid rgba(255,255,255,0.02); }
.pts { color: var(--cyan) !important; font-weight: 700; }

.section-hd { font-size: 9px; font-weight: 700; color: var(--cyan); letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 4. DATA ENGINE (ESPN API)
# ══════════════════════════════════════════════════════════════════════════════
now          = datetime.now()
SEASON_LABEL = f"{now.year}/{str(now.year + 1)[-2:]}"

LEAGUES = {
    "EPL": {"name": "Premier League", "espn": "eng.1"},
    "La Liga": {"name": "La Liga", "espn": "esp.1"},
    "Bundesliga": {"name": "Bundesliga", "espn": "ger.1"},
    "Serie A": {"name": "Serie A", "espn": "ita.1"},
    "UCL": {"name": "Champions League", "espn": "uefa.champions"},
}

@st.cache_data(ttl=1800)
def fetch_standings(league_code):
    try:
        url = f"https://site.api.espn.com/apis/v2/sports/soccer/{league_code}/standings"
        r = requests.get(url, timeout=10)
        data = r.json()
        entries = []
        for e in (data.get("children", [data])[0]).get("standings", {}).get("entries", []):
            stats = {s["name"]: s.get("value", 0) for s in e.get("stats", [])}
            entries.append({
                "rank": int(stats.get("rank", 0)),
                "name": e["team"]["displayName"],
                "pts": int(stats.get("points", 0))
            })
        return sorted(entries, key=lambda x: x["rank"])
    except: return []

# ══════════════════════════════════════════════════════════════════════════════
# 5. SIDEBAR & STATE
# ══════════════════════════════════════════════════════════════════════════════
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown('<p class="section-hd">System Intel</p>', unsafe_allow_html=True)
    sel_key = st.selectbox("Active League", options=list(LEAGUES.keys()), label_visibility="collapsed")
    sdata = fetch_standings(LEAGUES[sel_key]["espn"])
    
    # Quick View Standings
    table_body = "".join([f"<tr><td>{t['rank']}</td><td>{t['name']}</td><td class='pts'>{t['pts']}</td></tr>" for t in sdata[:8]])
    st.markdown(f"<table class='stbl'><thead><tr><th>#</th><th>CLUB</th><th>PTS</th></tr></thead><tbody>{table_body}</tbody></table>", unsafe_allow_html=True)
    
    if st.button("CLEAR CORE MEMORY"):
        st.session_state.messages = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# 6. SHADOW CHAT ENGINE (GROQ LLAMA 3.3 70B)
# ══════════════════════════════════════════════════════════════════════════════

# The Ground Truth for AI knowledge
SYSTEM_PROMPT = (
    "You are PITCH IQ, an elite football intelligence system. "
    "MANDATORY KNOWLEDGE: Cristiano Ronaldo plays for Al Nassr in Saudi Arabia. "
    "Lionel Messi plays for Inter Miami. Kylian Mbappé is at Real Madrid. "
    "Reference modern tactics and live data provided. Use bolding for emphasis."
)

# Display only the clean UI history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask PITCH IQ...")

if user_input:
    # 1. UI Display (Clean Message)
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Shadow Prompting (Enrich message for API, not for UI)
    top_5_list = ", ".join([f"{t['name']} ({t['pts']}pts)" for t in sdata[:5]])
    enriched_input = (
        f"[LIVE DATA - {LEAGUES[sel_key]['name']}]: {top_5_list}. "
        f"USER QUERY: {user_input}"
    )

    # 3. Construct Payload
    api_payload = [{"role": "system", "content": SYSTEM_PROMPT}]
    for m in st.session_state.messages[:-1]:
        api_payload.append(m)
    api_payload.append({"role": "user", "content": enriched_input})

    # 4. API Call
    with st.chat_message("assistant"):
        try:
            from groq import Groq
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=api_payload,
                temperature=0.3
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Intelligence Module Error: {e}")