import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="Football AI Assistant",
    page_icon="⚽",
    layout="wide"
)

# Load API key from Streamlit secrets
api_key = st.secrets["GROQ_API_KEY"]

# Initialize Groq client
client = Groq(api_key=api_key)

# App title
st.title("⚽ Football AI Assistant")

st.write(
    "Ask anything about football players, clubs, tactics, stats, or football history."
)

# Sidebar
with st.sidebar:

    st.header("⚽ Football AI")

    st.write("Powered by Groq + Llama 3.1")

    st.divider()

    st.subheader("Example Questions")

    st.write("- Compare Messi vs Ronaldo")
    st.write("- Best Premier League midfielders")
    st.write("- Guardiola tactics")
    st.write("- Cristiano Ronaldo stats")
    st.write("- Explain tiki-taka")

# Initialize conversation memory
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are an expert football AI assistant.

            Provide:
            - player stats
            - tactical analysis
            - football history
            - club information
            - trophies
            - comparisons
            - football trivia

            Keep answers engaging and informative.
            """
        }
    ]

# Display previous chat messages
for message in st.session_state.messages:

    if message["role"] != "system":

        st.chat_message(message["role"]).write(
            message["content"]
        )

# Chat input
user_input = st.chat_input(
    "Ask a football question..."
)

# Process user message
if user_input:

    # Display user message
    st.chat_message("user").write(user_input)

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # AI response
    with st.spinner("Analyzing football data..."):

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            temperature=0.3
        )

        assistant_reply = (
            response.choices[0]
            .message
            .content
        )

    # Display assistant response
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