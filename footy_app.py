import streamlit as st
from groq import Groq
import requests
from datetime import datetime

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Football AI Assistant",
    page_icon="⚽",
    layout="wide"
)

# ---------------------------------
# CUSTOM STYLING
# ---------------------------------

st.markdown(
    """
    <style>

    /* MAIN APP */

    .stApp {
        background-image:
        linear-gradient(
            rgba(0, 0, 0, 0.80),
            rgba(0, 0, 0, 0.90)
        ),
        url("https://images.unsplash.com/photo-1517466787929-bc90951d0974?q=80&w=2070&auto=format&fit=crop");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* REMOVE STREAMLIT HEADER */

    header {
        background: transparent !important;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background:
        linear-gradient(
            rgba(5, 5, 5, 0.96),
            rgba(15, 15, 15, 0.96)
        ),
        url("https://images.unsplash.com/photo-1522778119026-d647f0596c20?q=80&w=800&auto=format&fit=crop");

        background-size: cover;
        background-position: center;
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* TEXT */

    h1, h2, h3, h4, h5, h6, p, div, span {
        color: white;
    }

    /* CHAT MESSAGE */

    .stChatMessage {
        background-color: rgba(20, 20, 20, 0.72);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 14px;
        backdrop-filter: blur(10px);
    }

    /* FEATURE CARDS */

    .feature-card {
        background: rgba(20, 20, 20, 0.72);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 15px;
        border: 1px solid rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        transition: 0.3s ease;
    }

    .feature-card:hover {
        transform: scale(1.03);
        background: rgba(35, 35, 35, 0.92);
    }

    /* FLOATING BALL */

    @keyframes float {

        0% {
            transform: translateY(0px);
        }

        50% {
            transform: translateY(-8px);
        }

        100% {
            transform: translateY(0px);
        }
    }

    .football {
        animation: float 3s ease-in-out infinite;
        text-align: center;
        font-size: 75px;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# LOAD API KEYS
# ---------------------------------

groq_api_key = st.secrets["GROQ_API_KEY"]
football_api_key = st.secrets["FOOTBALL_API_KEY"]

# ---------------------------------
# API HEADERS
# ---------------------------------

headers = {
    "x-apisports-key": football_api_key
}

# ---------------------------------
# INITIALIZE GROQ
# ---------------------------------

client = Groq(api_key=groq_api_key)

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="football">
            ⚽
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 style='text-align:center;'>
            Football AI
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown(
        """
        <div class="feature-card">

        <h3>🧠 Smart Football Knowledge</h3>

        <p>
        Ask about players, clubs,
        football history, tactics,
        rivalries, and legendary matches.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="feature-card">

        <h3>💬 Conversational Memory</h3>

        <p>
        Ask follow-up questions naturally
        like a real football discussion.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="feature-card">

        <h3>⚡ Fast AI Responses</h3>

        <p>
        Powered by Groq + Llama 3.1
        for instant football analysis.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("🔥 Example Questions")

    st.write("• Messi vs Ronaldo")
    st.write("• Best Premier League midfielders")
    st.write("• Guardiola tactics")
    st.write("• Wayne Rooney career")
    st.write("• Last El Clasico")
    st.write("• Arsenal current squad")

# ---------------------------------
# TITLE SECTION
# ---------------------------------

st.markdown(
    """
    <div style="padding-top:10px;">

        <h1 style="
            font-size:72px;
            font-weight:800;
            margin-bottom:10px;
        ">
            ⚽ Football AI Assistant
        </h1>

        <p style="
            font-size:24px;
            color:#d1d1d1;
            margin-top:0px;
        ">
            Get live football stats,
            tactical analysis,
            player insights,
            and football intelligence.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------
# CHAT MEMORY
# ---------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are an elite football AI analyst.

            You provide:
            - tactical analysis
            - player analysis
            - football insights
            - club analysis
            - comparisons
            - football history

            Speak naturally and confidently.
            """
        }
    ]

# ---------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------

for message in st.session_state.messages:

    if message["role"] != "system":

        st.chat_message(
            message["role"]
        ).write(message["content"])

# ---------------------------------
# USER INPUT
# ---------------------------------

user_input = st.chat_input(
    "Ask anything about football..."
)

# ---------------------------------
# PROCESS INPUT
# ---------------------------------

if user_input:

    st.chat_message("user").write(user_input)

    # ---------------------------------
    # CURRENT SEASON
    # ---------------------------------

    today = datetime.now()

    if today.month >= 7:
        current_season = today.year
    else:
        current_season = today.year - 1

    # ---------------------------------
    # FOOTBALL API
    # ---------------------------------

    url = (
        f"https://v3.football.api-sports.io/players"
        f"?search={user_input}&season={current_season}"
    )

    football_data = {}

    try:

        football_response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        football_data = football_response.json()

    except Exception as e:

        football_data = {
            "error": str(e)
        }

    # ---------------------------------
    # CHECK API DATA
    # ---------------------------------

    api_has_data = False

    if isinstance(football_data, dict):

        if (
            "response" in football_data
            and isinstance(
                football_data["response"],
                list
            )
            and len(football_data["response"]) > 0
        ):

            api_has_data = True

    # ---------------------------------
    # PROMPT ENGINEERING
    # ---------------------------------

    if api_has_data:

        prompt = f"""
        User Question:
        {user_input}

        Live Football API Data:
        {football_data}

        Use this football data naturally.

        Include:
        - overview
        - important stats
        - tactical analysis
        - interesting insights
        """

    else:

        prompt = f"""
        User Question:
        {user_input}

        No useful live football API data was found.

        Use your football knowledge naturally.

        Do NOT mention:
        - API limitations
        - subscription restrictions
        - missing API data

        Simply answer like a football expert.

        Include:
        - overview
        - career highlights
        - tactical analysis
        - interesting insights
        """

    # ---------------------------------
    # SAVE TO MEMORY
    # ---------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # ---------------------------------
    # GENERATE RESPONSE
    # ---------------------------------

    with st.spinner("⚽ Analyzing football knowledge..."):

        try:

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=st.session_state.messages,
                temperature=0.3
            )

            assistant_reply = (
                response
                .choices[0]
                .message
                .content
            )

        except Exception as e:

            assistant_reply = (
                f"Error generating response: {str(e)}"
            )

    # ---------------------------------
    # DISPLAY RESPONSE
    # ---------------------------------

    st.chat_message("assistant").write(
        assistant_reply
    )

    # ---------------------------------
    # SAVE RESPONSE
    # ---------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )