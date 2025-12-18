"""Streamlit demo: simple chat UI that forwards text to Dialogflow detectIntent."""
import streamlit as st
from dialogflow_client import detect_intent_text
import os

PROJECT_ID = os.environ.get("DIALOGFLOW_PROJECT_ID")

st.title("Dialogflow Chat Demo")
if not PROJECT_ID:
    st.error("Set environment variable DIALOGFLOW_PROJECT_ID to your Dialogflow project ID.")

if "history" not in st.session_state:
    st.session_state.history = []

with st.form(key="msg_form"):
    msg = st.text_input("You", key="msg_input")
    submit = st.form_submit_button("Send")

if submit and msg:
    res = detect_intent_text(PROJECT_ID, msg)
    user_line = f"You: {res['query_text']}"
    bot_line = f"Bot: {res['fulfillment_text']} (intent: {res['intent']}, conf: {res['confidence']:.2f})"
    st.session_state.history.append((user_line, bot_line))

for u, b in st.session_state.history:
    st.write(u)
    st.write(b)
