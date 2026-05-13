import streamlit as st
from groq import Groq

# Load API key
with open("/Users/survesh/Downloads/ey-ai-upskill-b4-11052026-main/key_vault/Groq/Key.txt", "r") as file:
    api_key = file.read().strip()

# Initialize Groq client
client = Groq(api_key=api_key)

# App title
st.title("⚽ Football AI Assistant")

st.write("Ask anything about football players, clubs, stats, tactics, or history.")

# Initialize chat memory
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are an expert football AI assistant.

            Provide:
            - player stats
            - club history
            - tactical analysis
            - trophies
            - comparisons
            - football trivia

            Keep answers clear and engaging.
            """
        }
    ]

# User input
user_input = st.chat_input("Ask a football question...")

# If user enters message
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

    # Send to Groq
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=st.session_state.messages,
        temperature=0.3
    )

    assistant_reply = response.choices[0].message.content

    # Display AI response
    st.chat_message("assistant").write(assistant_reply)

    # Store assistant reply
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )