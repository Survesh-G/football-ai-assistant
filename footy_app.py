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
# CUSTOM UI / UX STYLING
# ---------------------------------

st.markdown(
    """
    <style>

    /* Main background */

    .stApp {
        background-image:
        linear-gradient(
            rgba(0, 0, 0, 0.78),
            rgba(0, 0, 0, 0.88)
        ),
        url("https://images.unsplash.com/photo-1518604666860-9ed391f76460?q=80&w=2070&auto=format&fit=crop");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Remove white header */

    header {
        background: transparent !important;
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background: rgba(8, 8, 8, 0.92);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Text */

    h1, h2, h3, h4, h5, h6, p, div, span {
        color: white;
    }

    /* Chat cards */

    .stChatMessage {
        background-color: rgba(20, 20, 20, 0.72);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 18px;
        padding: 14px;
        margin-bottom: 14px;
        backdrop-filter: blur(8px);
    }

    /* Feature cards */

    .feature-card {
        background: rgba(25, 25, 25, 0.75);
        padding: 18px;
        border-radius: 18px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.05);
        margin-bottom: 15px;
        transition: 0.3s ease;
    }

    .feature-card:hover {
        transform: scale(1.03);
        background: rgba(40, 40, 40, 0.9);
    }

    /* Floating animation */

    @keyframes float {
        0% {
            transform: translateY(0px);
        }

        50% {
            transform: translateY(-6px);
        }

        100% {
            transform: translateY(0px);
        }
    }

    .floating-ball {
        animation: float 3s ease-in-out infinite;
        text-align: center;
        font-size: 70px;
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
# INITIALIZE GROQ CLIENT
# ---------------------------------

client = Groq(api_key=groq_api_key)

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:

    st.markdown(
        """
        <div class="floating-ball">
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
            <h3>⚡ Live AI Analysis</h3>
            <p>
            Tactical breakdowns, player analysis,
            and football intelligence powered by AI.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="feature-card">
            <h3>📊 Football Knowledge</h3>
            <p>
            Ask about players, clubs,
            football history, and tactics.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="feature-card">
            <h3>🧠 Conversational Memory</h3>
            <p>
            Ask follow-up questions naturally
            like a real football discussion.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("🔥 Example Questions")

    st.write("• Compare Messi vs Ronaldo")
    st.write("• Wayne Rooney career")
    st.write("• Guardiola tactics")
    st.write("• Last El Clasico")
    st.write("• Arsenal current squad")
    st.write("• Best Premier League midfielders")

# ---------------------------------
# TITLE SECTION
# ---------------------------------

st.markdown(
    """
    <div style="padding-top:20px;">
        <h1 style="font-size:72px;">
            ⚽ Football AI Assistant
        </h1>

        <p style="font-size:24px; color:#d1d1d1;">
            Get live football stats, tactical analysis,
            player insights, and football intelligence.
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

    # Display user message
    st.chat_message("user").write(user_input)

    # ---------------------------------
    # CURRENT FOOTBALL SEASON
    # ---------------------------------

    today = datetime.now()

    if today.month >= 7:
        current_season = today.year
    else:
        current_season = today.year - 1

    # ---------------------------------
    # FOOTBALL API REQUEST
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
    # CHECK IF API RETURNED DATA
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

        Use this live football data naturally.

        Include:
        - overview
        - important stats
        - tactical analysis
        - interesting insights

        Keep the tone engaging.
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
        - outdated information

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
    # GENERATE AI RESPONSE
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