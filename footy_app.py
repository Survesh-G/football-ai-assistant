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
# LOAD API KEYS
# ---------------------------------

groq_api_key = st.secrets["GROQ_API_KEY"]
football_api_key = st.secrets["FOOTBALL_API_KEY"]

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

    st.subheader("Example Questions")

    st.write("- Cristiano Ronaldo stats")
    st.write("- Messi vs Ronaldo")
    st.write("- Wayne Rooney career")
    st.write("- Guardiola tactics")
    st.write("- Last El Clasico")

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

            Keep responses engaging and natural.
            """
        }
    ]

# ---------------------------------
# DISPLAY OLD MESSAGES
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
    "Ask about football players, clubs, matches, or tactics..."
)

# ---------------------------------
# PROCESS USER INPUT
# ---------------------------------

if user_input:

    # Display user message
    st.chat_message("user").write(user_input)

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # ---------------------------------
    # FETCH LIVE FOOTBALL DATA
    # ---------------------------------

    headers = {
        "x-apisports-key": football_api_key
    }

    # Dynamic football season logic
    today = datetime.now()

    if today.month >= 7:
        current_season = today.year
    else:
        current_season = today.year - 1

    # API URL
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
    # SAFELY CHECK API DATA
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

        Use this live football data to answer naturally.

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

        Use your football knowledge to answer naturally.

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
    # GENERATE AI RESPONSE
    # ---------------------------------

    with st.spinner("Analyzing football data..."):

        try:

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
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

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )