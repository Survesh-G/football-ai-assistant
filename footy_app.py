
import streamlit as st
from groq import Groq
import requests
from datetime import datetime
import streamlit.components.v1 as components

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Football AI Assistant",
    page_icon="⚽",
    layout="wide"
)

# ---------------------------------
# GLOBAL CSS (safe to inject via markdown)
# ---------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600&display=swap');

    /* MAIN APP BACKGROUND */
    .stApp {
        background-image:
            linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.92)),
            url("https://images.unsplash.com/photo-1518091043644-c1d4457512c6?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }

    /* REMOVE STREAMLIT HEADER */
    header { background: transparent !important; }
    .block-container { padding-top: 1.5rem; }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background: linear-gradient(160deg, rgba(8,8,8,0.97), rgba(18,18,18,0.97));
        border-right: 1px solid rgba(255,255,255,0.07);
    }

    /* ALL TEXT */
    h1, h2, h3, h4, h5, h6, p, div, span, label { color: white; }

    /* CHAT MESSAGE */
    .stChatMessage {
        background-color: rgba(20,20,20,0.75) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 16px !important;
        padding: 14px !important;
        margin-bottom: 12px !important;
        backdrop-filter: blur(12px) !important;
    }

    /* CHAT INPUT */
    .stChatInputContainer {
        background: rgba(15,15,15,0.85) !important;
        border-top: 1px solid rgba(255,255,255,0.07) !important;
        border-radius: 16px !important;
        backdrop-filter: blur(10px) !important;
    }

    /* FEATURE CARDS */
    .feature-card {
        background: rgba(22,22,22,0.75);
        border-radius: 16px;
        padding: 16px 18px;
        margin-bottom: 14px;
        border: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(10px);
        transition: transform 0.25s ease, background 0.25s ease;
    }
    .feature-card:hover {
        transform: scale(1.03);
        background: rgba(38,38,38,0.92);
    }
    .feature-card h3 { font-size: 15px; margin-bottom: 6px; }
    .feature-card p  { font-size: 13px; color: #b0b0b0; margin: 0; }

    /* FLOATING FOOTBALL ANIMATION */
    @keyframes float {
        0%   { transform: translateY(0px); }
        50%  { transform: translateY(-9px); }
        100% { transform: translateY(0px); }
    }
    .football {
        animation: float 3s ease-in-out infinite;
        text-align: center;
        font-size: 72px;
        margin: 10px 0 4px 0;
    }

    /* EXAMPLE QUESTION PILLS */
    .pill {
        display: inline-block;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 999px;
        padding: 4px 12px;
        font-size: 12px;
        color: #d0d0d0;
        margin: 3px 2px;
    }

    /* SPINNER TEXT */
    .stSpinner > div { color: white !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# LOAD API KEYS
# ---------------------------------

groq_api_key    = st.secrets["GROQ_API_KEY"]
football_api_key = st.secrets["FOOTBALL_API_KEY"]

headers = {"x-apisports-key": football_api_key}

# ---------------------------------
# INITIALIZE GROQ
# ---------------------------------

client = Groq(api_key=groq_api_key)

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:
    st.markdown('<div class="football">⚽</div>', unsafe_allow_html=True)
    st.markdown(
        '<h1 style="text-align:center;font-family:\'Bebas Neue\',sans-serif;'
        'font-size:32px;letter-spacing:2px;color:white;margin-top:4px;">Football AI</h1>',
        unsafe_allow_html=True
    )
    st.write("")

    for icon, title, desc in [
        ("🧠", "Smart Football Knowledge",
         "Players, clubs, history, tactics, rivalries, and legendary matches."),
        ("💬", "Conversational Memory",
         "Ask follow-up questions naturally — like a real football discussion."),
        ("⚡", "Fast AI Responses",
         "Powered by Groq + Llama 3.1 for instant football analysis."),
    ]:
        st.markdown(
            f'<div class="feature-card">'
            f'<h3>{icon} {title}</h3>'
            f'<p>{desc}</p>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.divider()
    st.markdown(
        '<p style="font-size:13px;color:#888;margin-bottom:8px;">🔥 Example Questions</p>',
        unsafe_allow_html=True
    )
    for q in [
        "Messi vs Ronaldo", "Best Premier League midfielders",
        "Guardiola tactics", "Wayne Rooney career",
        "Last El Clasico", "Arsenal current squad"
    ]:
        st.markdown(f'<span class="pill">• {q}</span>', unsafe_allow_html=True)

    st.write("")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# ---------------------------------
# HERO HEADER  ← use components.html to avoid markdown parser issues
# ---------------------------------

components.html(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600&display=swap');
      * { margin:0; padding:0; box-sizing:border-box; }
      body { background: transparent; }

      .hero {
        background: rgba(12,12,12,0.72);
        padding: 32px 36px 28px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.06);
        backdrop-filter: blur(14px);
        margin-bottom: 6px;
      }
      .hero-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 68px;
        letter-spacing: 2px;
        color: #ffffff;
        line-height: 1;
        margin-bottom: 12px;
      }
      .hero-title span { color: #4ade80; }
      .hero-sub {
        font-family: 'Inter', sans-serif;
        font-size: 18px;
        color: #c8c8c8;
        line-height: 1.6;
        margin-bottom: 14px;
        font-weight: 300;
      }
      .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(74,222,128,0.12);
        border: 1px solid rgba(74,222,128,0.3);
        border-radius: 999px;
        padding: 5px 14px;
        font-family: 'Inter', sans-serif;
        font-size: 13px;
        color: #4ade80;
        font-weight: 500;
      }
      .dot { width:7px; height:7px; border-radius:50%; background:#4ade80;
             animation: pulse 1.8s ease-in-out infinite; display:inline-block; }
      @keyframes pulse {
        0%,100% { opacity:1; transform:scale(1); }
        50%      { opacity:0.4; transform:scale(0.75); }
      }
    </style>

    <div class="hero">
      <div class="hero-title">⚽ Football <span>AI</span> Assistant</div>
      <div class="hero-sub">
        Live stats · Tactical breakdowns · Player intelligence · Football history
      </div>
      <div class="hero-badge">
        <span class="dot"></span>
        Live data — 2025 Season
      </div>
    </div>
    """,
    height=210,
    scrolling=False
)

# ---------------------------------
# CHAT MEMORY
# ---------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are an elite football AI analyst with deep expertise across world football. "
                "You provide tactical analysis, player analysis, club history, comparisons, and insights. "
                "Be confident, opinionated, and engaging — like a knowledgeable pundit. "
                "Use stats when available. Format responses with clear sections using **bold headers** "
                "and bullet points for readability. Keep responses focused and sharp."
            )
        }
    ]

# ---------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ---------------------------------
# USER INPUT
# ---------------------------------

user_input = st.chat_input("Ask anything about football...")

# ---------------------------------
# PROCESS INPUT
# ---------------------------------

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    # ── Determine current season ──────────────────────────────────────
    today = datetime.now()
    current_season = today.year if today.month >= 7 else today.year - 1

    # ── Football API call ─────────────────────────────────────────────
    football_data = {}
    api_has_data   = False

    try:
        url = (
            f"https://v3.football.api-sports.io/players"
            f"?search={user_input}&season={current_season}"
        )
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        football_data = resp.json()

        if (
            isinstance(football_data.get("response"), list)
            and len(football_data["response"]) > 0
        ):
            api_has_data = True

    except requests.exceptions.RequestException as e:
        football_data = {"error": str(e)}

    # ── Build prompt ──────────────────────────────────────────────────
    if api_has_data:
        prompt = (
            f"User Question: {user_input}\n\n"
            f"Live Football API Data:\n{football_data}\n\n"
            "Use this data naturally. Include: overview, key stats, "
            "tactical analysis, and interesting insights. "
            "Format with **bold headers** and bullet points."
        )
    else:
        prompt = (
            f"User Question: {user_input}\n\n"
            "Answer from your football knowledge as an elite analyst. "
            "Do NOT mention API limitations, subscriptions, or data issues. "
            "Include: overview, career/club highlights, tactical analysis, insights. "
            "Format with **bold headers** and bullet points."
        )

    # ── Add to memory & generate response ────────────────────────────
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("⚽ Analysing..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=st.session_state.messages,
                    temperature=0.35,
                    max_tokens=1024,
                )
                reply = response.choices[0].message.content

            except Exception as e:
                reply = f"⚠️ Error generating response: {str(e)}"

        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})