"""Streamlit application."""

import os

import streamlit as st

from agent import query_agent

# App title
st.set_page_config(page_title="searchagent")

# Credentials
with st.sidebar:
    st.title("searchagent")
    st.subheader("Credentials")

    if "OPENAI_API_KEY" in st.secrets:
        st.success("API key provided!", icon="✅")
        openai_key = st.secrets["OPENAI_API_KEY"]
    else:
        openai_key = st.text_input("Enter OpenAI API token:", type="password")
        if not (len(openai_key) == 164):  # noqa: PLR2004
            st.warning("Please enter your credentials!", icon="⚠️")
        else:
            st.success("Proceed to entering your prompt message!", icon="👉")

os.environ["OPENAI_API_KEY"] = openai_key

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]


def clear_chat_history():
    """Reset chat history."""
    st.session_state.messages = [
        {"role": "assistant", "content": "How may I assist you today?"}
    ]


st.sidebar.button("Clear Chat History", on_click=clear_chat_history)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me anything"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.spinner("Please wait...", show_time=True):
            response = query_agent(prompt)

        with st.chat_message("assistant"):
            if isinstance(response, str) and response[-10:] == "image.webp":
                st.image(response)
            else:
                st.markdown(response)

            # Add assistant response to chat history
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
    except Exception as e:
        st.exception(f"An error occurred: {e}")
