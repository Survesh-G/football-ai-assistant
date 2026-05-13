import streamlit as st
from groq import Groq
import requests

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="Football AI Assistant",
    page_icon="⚽",
    layout="wide"
)

# ---------------------------------
# LOAD API KEYS FROM STREAMLIT SECRETS
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
    st.write("- Arsenal current form")
    st.write("- Guardiola tactics")
    st.write("- Mbappe current club")

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
            - comparisons
            - football history
            - football insights

            Keep responses engaging and informative.
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
    "Ask about football players, clubs, or tactics..."
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

    url = (
        f"https://v3.football.api-sports.io/players"
        f"?search={user_input}&season=2024"
    )

    try:

        football_response = requests.get(
            url,
            headers=headers
        )

        football_data = football_response.json()

    except Exception as e:

        football_data = {
            "error": str(e)
        }

    # ---------------------------------
    # CREATE AI PROMPT
    # ---------------------------------

    prompt = f"""
    User Question:
    {user_input}

    Live Football Data:
    {football_data}

    Analyze this football information clearly.

    Include:
    - overview
    - important stats
    - tactical analysis
    - interesting insights
    """

    # ---------------------------------
    # GENERATE AI RESPONSE
    # ---------------------------------

    with st.spinner("Analyzing football data..."):

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

    # ---------------------------------
    # DISPLAY RESPONSE
    # ---------------------------------

    st.chat_message("assistant").write(
        assistant_reply
    )

    # Save response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )