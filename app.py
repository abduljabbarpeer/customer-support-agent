"""
A simple chat page for DemoKart customers, made with Streamlit.

Run it on your laptop with:  .venv/bin/streamlit run app.py

Settings (GOOGLE_API_KEY, GEMINI_MODEL, APP_PASSCODE ...) come from .env on your laptop.
Online, they come from Streamlit secrets, which Streamlit also puts into environment
variables, so the code below just reads environment variables in both places.
"""

import asyncio
import hmac
import os
import uuid

import streamlit as st
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

# Read .env if it exists (laptop). Online there is no .env and this does nothing.
load_dotenv()

# Our existing agent, and the help-docs index folder.
from support_agent.agent import root_agent
from support_agent.help_docs import CHROMA_DIR, build_index

APP_NAME = "demokart_support"

st.set_page_config(page_title="DemoKart Support", page_icon="💬")
st.title("DemoKart Support")


@st.cache_resource
def start_up():
    """Runs once when the app starts: build the help-docs index if it is missing, make the runner."""
    # chroma_db is not uploaded online, so build it once the first time.
    if not CHROMA_DIR.exists():
        build_index()
    # The runner runs the agent and keeps the conversations in memory.
    return InMemoryRunner(agent=root_agent, app_name=APP_NAME)


# ---- 1. Passcode box: the chat only appears after the right passcode ----
passcode = os.environ.get("APP_PASSCODE", "")
if not passcode:
    st.error("This page is not set up yet: the APP_PASSCODE setting is missing.")
    st.stop()

if not st.session_state.get("unlocked"):
    entered = st.text_input("Passcode", type="password")
    if entered:
        if hmac.compare_digest(entered.encode(), passcode.encode()):
            st.session_state["unlocked"] = True
            st.rerun()
        else:
            st.error("That passcode is not right.")
    st.stop()

# ---- 2. The chat ----
with st.spinner("Starting up..."):
    runner = start_up()

# One conversation per browser session: each visitor gets their own ids and message list.
if "session_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())
    st.session_state["session_id"] = str(uuid.uuid4())
    st.session_state["messages"] = []
    asyncio.run(
        runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=st.session_state["user_id"],
            session_id=st.session_state["session_id"],
        )
    )


async def ask_agent(text):
    """Send one message to the agent and return its final reply as text."""
    message = types.Content(role="user", parts=[types.Part(text=text)])
    reply = ""
    async for event in runner.run_async(
        user_id=st.session_state["user_id"],
        session_id=st.session_state["session_id"],
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            reply = "".join(p.text or "" for p in event.content.parts)
    return reply


# Show the conversation so far.
for m in st.session_state["messages"]:
    with st.chat_message(m["role"]):
        st.markdown(m["text"])

# Take a new message, send it to the agent and show the reply.
if question := st.chat_input("How can we help?"):
    st.session_state["messages"].append({"role": "user", "text": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = asyncio.run(ask_agent(question))
            except Exception:
                answer = "Sorry, something went wrong. Please try again."
        st.markdown(answer or "Sorry, I have no reply right now.")
    st.session_state["messages"].append({"role": "assistant", "text": answer})
