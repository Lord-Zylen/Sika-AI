"""Sika AI — Streamlit chat interface."""

import streamlit as st
from main import chat

st.set_page_config(page_title="Sika AI", page_icon="GH", layout="centered")
st.title("Sika AI")
st.caption("Your Ghana financial assistant")

# Session state for conversation history
if "history" not in st.session_state:
    st.session_state.history = []

# Display existing messages
for msg in st.session_state.history:
    role = msg["role"]
    with st.chat_message(role):
        st.markdown(msg["content"])

# User input
if prompt := st.chat_input("Ask me anything about finances in Ghana..."):
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                reply, updated_history = chat(prompt, st.session_state.history)
                st.session_state.history = updated_history
                st.markdown(reply)
            except Exception as e:
                st.error(f"Error: {e}")
                st.session_state.history.append({"role": "user", "content": prompt})

# Sidebar
with st.sidebar:
    st.header("Sika AI")
    st.markdown("Financial assistant for Ghana")
    st.divider()
    if st.button("Clear conversation"):
        st.session_state.history = []
        st.rerun()
    st.divider()
    st.caption("Powered by OpenAI GPT-4o")
    st.caption("Not a licensed financial advisor")
