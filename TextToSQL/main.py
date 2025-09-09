
import streamlit as st
from utils import invoke_chain
from followup_suggestion import get_followup_suggestions

st.title("Text To SQL Chatbot")

# Initialize chat history and current question
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "last_suggestions" not in st.session_state:
    st.session_state.last_suggestions = []
if "pending_followup" not in st.session_state:
    st.session_state.pending_followup = None

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    st.session_state.current_question = prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.spinner("Generating response..."):
        response = invoke_chain(prompt, st.session_state.messages)
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # error handling
    if "error" in response.lower():
        st.error(response)
        if st.button("Start New Conversation"):
            st.session_state.messages = []
            st.session_state.current_question = None
            st.session_state.last_suggestions = []
            st.session_state.pending_followup = None
            st.rerun()

    # Get follow-up suggestions in parallel (after response)
    with st.spinner("Getting follow-up suggestions..."):
        suggestions = get_followup_suggestions(prompt)
    st.session_state.last_suggestions = suggestions

# Handle follow-up button click (after rerun)
if st.session_state.pending_followup:
    followup = st.session_state.pending_followup
    st.session_state.current_question = followup
    st.session_state.messages.append({"role": "user", "content": followup})
    with st.chat_message("user"):
        st.markdown(followup)
    with st.spinner("Generating response..."):
        followup_response = invoke_chain(followup, st.session_state.messages)
    with st.chat_message("assistant"):
        st.markdown(followup_response)
    st.session_state.messages.append({"role": "assistant", "content": followup_response})

    # error handling for follow-up
    if "error" in followup_response.lower():
        st.error(followup_response)
        if st.button("Start New Conversation"):
            st.session_state.messages = []
            st.session_state.current_question = None
            st.session_state.last_suggestions = []
            st.session_state.pending_followup = None
            st.rerun()

    # Get new suggestions for the follow-up
    with st.spinner("Getting follow-up suggestions..."):
        st.session_state.last_suggestions = get_followup_suggestions(followup)
    st.session_state.pending_followup = None

# Show follow-up suggestions for the latest question
if st.session_state.last_suggestions:
    st.markdown("**You might also ask:**")
    for i, followup in enumerate(st.session_state.last_suggestions):
        if isinstance(followup, str) and followup.strip():
            if st.button(followup, key=f"{followup}_{i}"):
                st.session_state.pending_followup = followup
                st.rerun()
