from groq import Groq

# Read API key
with open("/Users/survesh/Downloads/ey-ai-upskill-b4-11052026-main/key_vault/Groq/Key.txt", "r") as file:
    api_key = file.read().strip()

# Initialize Groq client
client = Groq(api_key=api_key)

print("\n⚽ Football AI Assistant Started!")
print("Type 'exit' anytime to quit.\n")

# Conversation history
messages = [
    {
        "role": "system",
        "content": """
        You are an expert football AI assistant.

        You provide:
        - player information
        - football stats
        - tactical analysis
        - club history
        - trophies
        - comparisons
        - football trivia

        Keep answers clear and engaging.
        """
    }
]

# Continuous chat loop
while True:

    user_input = input("You: ")

    # Exit condition
    if user_input.lower() == "exit":
        print("\nGoodbye ⚽")
        break

    # Add user message
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Send to Groq
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3
    )

    assistant_reply = response.choices[0].message.content

    # Print response
    print("\nFootball AI:")
    print(assistant_reply)
    print()

    # Store assistant reply
    messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )