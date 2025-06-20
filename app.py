import streamlit as st
from streamlit_chat import message
import puter

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar for model selection
with st.sidebar:
    st.header("AI Configuration")
    model = st.selectbox(
        "Select Model",
        ("Claude 3.5", "Llama 3.1", "GPT-4o Mini"),
        index=0
    )
    
    st.info("Advanced reasoning, coding, and creative writing capabilities")

# Chat interface
st.title("🤖 AI Agent Afra")
st.caption(f"Using: {model}")

# Display chat history
for i, (speaker, msg) in enumerate(st.session_state.history):
    message(msg, is_user=(speaker == "user"), key=f"{i}_{speaker}")

# Input area
prompt = st.chat_input("Message AI Explorer...")
if prompt:
    # Add user message
    st.session_state.history.append(("user", prompt))
    
    # Get AI response
    with st.spinner("Thinking..."):
        response = puter.ai.chat(prompt, model=model.lower().replace(" ", "-"))
        st.session_state.history.append(("ai", response))
    
    st.rerun()
