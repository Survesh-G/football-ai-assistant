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
# CUSTOM BACKGROUND
# ---------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-image: linear-gradient(
            rgba(0, 0, 0, 0.82),
            rgba(0, 0, 0, 0.88)
        ),
        url("https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2070&auto=format&fit=crop");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    h1, h2, h3, h4, h5, h6, p, div {
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: rgba(15, 15, 15, 0.92);
    }

    .stChatMessage {
        background-color: rgba(25, 25, 25, 0.75);
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 10px;
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
# APP TITLE
# ---------------------------------

st.title("⚽ Football AI Assistant")

st.write(
    "Get live football stats, tactical analysis, player insights, and football knowledge."
)

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:

    st.header("⚽ Football AI")

    st.write("Powered by Groq + API-Football")

    st.divider()

    # ---------------------------------
    # DYNAMIC FOOTBALL SEASON
    # ---------------------------------

    today = datetime.now()

    if today.month >= 7:
        current_season = today.year
    else:
        current_season = today.year - 1

    # ---------------------------------
    # LIVE EPL TABLE
    # ---------------------------------

    st.subheader("📊 Live EPL Table")

    try:

        standings_url = (
            f"https://v3.football.api-sports.io/standings"
            f"?league=39&season={current_season}"
        )

        standings_response = requests.get(
            standings_url,
            headers=headers,
            timeout=10
        )

        standings_data = standings_response.json()

        table = (
            standings_data["response"][0]
            ["league"]["standings"][0]
        )

        for team in table[:10]:

            position = team["rank"]
            name = team["team"]["name"]
            points = team["points"]

            st.write(
                f"{position}. {name} — {points} pts"
            )

    except Exception:

        st.write("Unable to load EPL standings.")

    st.divider()

    st.subheader("🔥 Example Questions")

    st.write("- Cristiano Ronaldo stats")
    st.write("- Messi vs Ronaldo")
    st.write("- Wayne Rooney career")
    st.write("- Guardiola tactics")
    st.write("- Last El Clasico")
    st.write("- Arsenal current squad")

# ---------------------------------
# CHAT MEMORY
# ---------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are an expert football AI assistant.

            Use live football data whenever available.

            Provide:
            - player stats
            - tactical analysis
            - club information
            - football history
            - comparisons
            - football insights

            Keep responses engaging, concise, and natural.
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
    "Ask about football players, clubs, tactics, or matches..."
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
    # FETCH PLAYER DATA
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
    # VALIDATE API RESPONSE
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
    # CREATE PROMPT
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
    # SAVE ENHANCED PROMPT TO MEMORY
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

    with st.spinner("⚽ Analyzing football data..."):

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
    # DISPLAY AI RESPONSE
    # ---------------------------------

    st.chat_message("assistant").write(
        assistant_reply
    )

    # ---------------------------------
    # SAVE RESPONSE TO MEMORY
    # ---------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )