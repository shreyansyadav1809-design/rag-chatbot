import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="My AI Assistant",
    page_icon="🤖",
    layout="centered"
)


# =========================================================
# LOAD API KEY
# =========================================================

api_key = None


# ---------------------------------------------------------
# 1. Try Streamlit secrets
# ---------------------------------------------------------

try:

    api_key = st.secrets.get(
        "OPENROUTER_API_KEY"
    )

except Exception:

    api_key = None


# ---------------------------------------------------------
# 2. If not found, try .env
# ---------------------------------------------------------

if not api_key:

    BASE_DIR = Path(__file__).resolve().parent

    ENV_FILE = BASE_DIR / ".env"

    load_dotenv(ENV_FILE)

    api_key = os.getenv(
        "OPENROUTER_API_KEY"
    )


# =========================================================
# CHECK API KEY
# =========================================================

if not api_key:

    st.error(
        "❌ OPENROUTER_API_KEY not found.\n\n"
        "Please check your .env or "
        ".streamlit/secrets.toml file."
    )

    st.stop()


# =========================================================
# OPENROUTER CLIENT
# =========================================================

client = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key=api_key
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <h1 style="text-align:center;">
        🤖 My AI Assistant
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="text-align:center;">
        Powered by OpenRouter
    </p>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚙️ Settings")

    st.info(
        "Using OpenRouter Free Model"
    )

    st.write("### Features")

    st.write("✅ AI Chat")
    st.write("✅ Conversation Memory")
    st.write("✅ OpenRouter")
    st.write("✅ Free Model")
    st.write("✅ Streamlit UI")

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()


# =========================================================
# CHAT MEMORY
# =========================================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =========================================================
# DISPLAY OLD MESSAGES
# =========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =========================================================
# CHAT INPUT
# =========================================================

user_input = st.chat_input(
    "Ask me anything..."
)


# =========================================================
# PROCESS USER MESSAGE
# =========================================================

if user_input:

    # -----------------------------------------------------
    # Add user message
    # -----------------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # -----------------------------------------------------
    # Display user message
    # -----------------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_input)


    # -----------------------------------------------------
    # Generate AI response
    # -----------------------------------------------------

    with st.chat_message("assistant"):

        try:

            with st.spinner("Thinking..."):

                response = client.chat.completions.create(

                    model="openrouter/free",

                    messages=[
                        {
                            "role": "system",

                            "content": """
You are a helpful AI assistant.

Answer questions clearly and accurately.

You can help with:

- Python
- Programming
- AI
- Machine Learning
- Data Science
- Mathematics
- Science
- Career
- Projects
- General Knowledge
- Debugging
- Writing

Rules:

1. Be helpful.
2. Do not intentionally make up information.
3. If you don't know something, say so.
4. Explain difficult topics simply.
5. Give examples when useful.
6. If the user asks for code, provide working code.
7. If the user speaks Hinglish, respond naturally in Hinglish.
8. Keep answers relevant and easy to understand.
"""
                        },

                        *st.session_state.messages
                    ],

                    max_tokens=2000
                )


                # -----------------------------------------
                # Get answer
                # -----------------------------------------

                answer = (
                    response
                    .choices[0]
                    .message
                    .content
                )


            # ------------------------------------------------
            # Display answer
            # ------------------------------------------------

            st.markdown(answer)


            # ------------------------------------------------
            # Save answer
            # ------------------------------------------------

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )


        except Exception as e:

            st.error(
                "⚠️ OpenRouter Error"
            )

            with st.expander(
                "Show error"
            ):

                st.code(
                    str(e)
                )