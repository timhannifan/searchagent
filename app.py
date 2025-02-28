"""Streamlit application."""
 
import streamlit as st

from agent import query_agent

st.title("Agent Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.spinner("Please wait...", show_time=True):
            response = query_agent(prompt)
            
        with st.chat_message("assistant"):
            st.markdown(response)

            # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.exception(f"An error occurred: {e}")