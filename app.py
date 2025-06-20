import streamlit as st
import base64
import time

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'model' not in st.session_state:
    st.session_state.model = "Anthropic Claude 3.5 Sonnet"
if 'model_badge' not in st.session_state:
    st.session_state.model_badge = "Claude 3.5"

# Set page config
st.set_page_config(
    page_title="AI Agent Afra",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown(f"""
<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
}}

:root {{
    --primary: #10a37f;
    --primary-dark: #0d8c6d;
    --light-bg: #f7f7f8;
    --card-bg: #ffffff;
    --sidebar-bg: #f0f0f0;
    --text-primary: #343541;
    --text-secondary: #6e6e80;
    --user-msg: #f7f7f8;
    --ai-msg: #ffffff;
    --input-bg: #ffffff;
    --border: #e5e5e5;
    --shadow: rgba(0, 0, 0, 0.05);
    --shadow-md: rgba(0, 0, 0, 0.1);
    --success: #10b981;
    --error: #ef4444;
}}

body {{
    background-color: var(--light-bg);
    color: var(--text-primary);
}}

.main {{
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 900px;
    margin: 0 auto;
    padding: 0;
}}

.top-bar {{
    padding: 15px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid var(--border);
    background-color: var(--card-bg);
    box-shadow: 0 1px 3px var(--shadow);
    z-index: 10;
}}

.model-display {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1rem;
}}

.model-badge {{
    background-color: var(--primary);
    color: white;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
}}

.controls {{
    display: flex;
    gap: 15px;
}}

.control-btn {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--input-bg);
    border: 1px solid var(--border);
    color: var(--text-secondary);
    cursor: pointer;
    transition: all 0.2s;
}}

.control-btn:hover {{
    background-color: #eaeaea;
    color: var(--text-primary);
}}

.chat-container {{
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 20px;
    background-color: var(--light-bg);
}}

.message {{
    max-width: 90%;
    display: flex;
    gap: 15px;
    animation: fadeIn 0.3s ease-out;
}}

@keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(10px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.message.user {{
    align-self: flex-end;
}}

.avatar {{
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-weight: 600;
    background-color: var(--primary);
    color: white;
    font-size: 0.9rem;
}}

.ai .avatar {{
    background-color: #9d9da8;
}}

.message-content {{
    padding: 15px 20px;
    border-radius: 18px;
    line-height: 1.5;
    box-shadow: 0 2px 8px var(--shadow);
    background-color: var(--card-bg);
    border: 1px solid var(--border);
    font-size: 1rem;
}}

.user .message-content {{
    background-color: var(--primary);
    color: white;
    border-bottom-right-radius: 5px;
}}

.ai .message-content {{
    background-color: var(--ai-msg);
    border-bottom-left-radius: 5px;
}}

.input-container {{
    padding: 15px 20px;
    position: relative;
    background-color: var(--card-bg);
    border-top: 1px solid var(--border);
    box-shadow: 0 -1px 3px var(--shadow);
}}

.input-box {{
    position: relative;
    max-width: 800px;
    margin: 0 auto;
}}

.chat-input {{
    width: 100%;
    padding: 16px 55px 16px 20px;
    border-radius: 24px;
    background-color: var(--input-bg);
    border: 1px solid var(--border);
    color: var(--text-primary);
    font-size: 1rem;
    resize: none;
    min-height: 56px;
    max-height: 150px;
    outline: none;
    transition: border 0.3s;
    box-shadow: 0 2px 8px var(--shadow);
}}

.chat-input:focus {{
    border-color: var(--primary);
}}

.send-btn {{
    position: absolute;
    right: 15px;
    bottom: 12px;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background-color: var(--primary);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
}}

.send-btn:hover {{
    background-color: var(--primary-dark);
    transform: scale(1.05);
}}

.send-btn:disabled {{
    background-color: #c2c2c2;
    cursor: not-allowed;
    transform: none;
}}

.typing-indicator {{
    display: flex;
    align-items: center;
    gap: 5px;
    color: var(--text-secondary);
    font-size: 0.9rem;
    padding: 15px 0 0 55px;
}}

.typing-dots {{
    display: flex;
    gap: 3px;
}}

.typing-dots span {{
    width: 6px;
    height: 6px;
    background-color: var(--text-secondary);
    border-radius: 50%;
    display: inline-block;
    animation: typing 1.4s infinite ease-in-out;
}}

.typing-dots span:nth-child(1) {{ animation-delay: 0s; }}
.typing-dots span:nth-child(2) {{ animation-delay: 0.2s; }}
.typing-dots span:nth-child(3) {{ animation-delay: 0.4s; }}

@keyframes typing {{
    0%, 60%, 100% {{ transform: translateY(0); }}
    30% {{ transform: translateY(-4px); }}
}}

.welcome-container {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 20px;
}}

.welcome-container h1 {{
    font-size: 2.2rem;
    margin-bottom: 20px;
    color: var(--text-primary);
    font-weight: 700;
}}

.welcome-container h1 span {{
    color: var(--primary);
}}

.welcome-container p {{
    max-width: 600px;
    line-height: 1.6;
    color: var(--text-secondary);
    margin-bottom: 30px;
    font-size: 1.1rem;
}}

@media (max-width: 768px) {{
    .message {{
        max-width: 85%;
    }}
    
    .welcome-container h1 {{
        font-size: 1.8rem;
    }}
    
    .welcome-container p {{
        font-size: 1rem;
        padding: 0 15px;
    }}
}}

@media (max-width: 480px) {{
    .top-bar {{
        padding: 12px 15px;
    }}
    
    .model-badge {{
        padding: 4px 10px;
        font-size: 0.7rem;
    }}
    
    .chat-container {{
        padding: 15px 10px;
        gap: 15px;
    }}
    
    .message-content {{
        padding: 12px 16px;
        font-size: 0.95rem;
    }}
    
    .avatar {{
        width: 32px;
        height: 32px;
        font-size: 0.8rem;
    }}
    
    .input-container {{
        padding: 12px 15px;
    }}
    
    .chat-input {{
        padding: 14px 50px 14px 16px;
        min-height: 80px;
        font-size: 0.95rem;
    }}
    
    .send-btn {{
        width: 30px;
        height: 30px;
        right: 12px;
        bottom: 11px;
    }}
}}
</style>
""", unsafe_allow_html=True)

# Sidebar equivalent using Streamlit
with st.sidebar:
    st.header("AI Configuration")
    st.session_state.model = st.selectbox(
        "Select AI Model",
        (
            "Meta Llama 3.1 (8B)",
            "Anthropic Claude 3.5 Sonnet",
            "Mistral 7B",
            "Google Gemini Pro 1.5",
            "OpenAI GPT-4o Mini"
        ),
        index=1
    )
    
    # Update model badge
    if "Llama" in st.session_state.model:
        st.session_state.model_badge = "Llama 3.1"
    elif "Claude" in st.session_state.model:
        st.session_state.model_badge = "Claude 3.5"
    elif "Mistral" in st.session_state.model:
        st.session_state.model_badge = "Mistral 7B"
    elif "Gemini" in st.session_state.model:
        st.session_state.model_badge = "Gemini 1.5"
    elif "GPT" in st.session_state.model:
        st.session_state.model_badge = "GPT-4o"
    
    st.info(f"**Current Model:** {st.session_state.model}")
    st.info("**Capabilities:** Advanced reasoning, coding, creative writing")

# Main app layout
st.markdown('<div class="main">', unsafe_allow_html=True)

# Top bar
st.markdown("""
<div class="top-bar">
    <div class="model-display">
        <div class="model-badge">{model_badge}</div>
        <div id="model-status">Ready</div>
    </div>
    <div class="controls">
        <div class="control-btn" title="Clear Chat" id="clear-chat">
            <i class="fas fa-trash"></i>
        </div>
    </div>
</div>
""".format(model_badge=st.session_state.model_badge), unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container" id="chat-container">', unsafe_allow_html=True)

# Welcome message for new chats
if len(st.session_state.history) == 0:
    st.markdown("""
    <div class="welcome-container">
        <h1>AI Model <span>Explorer</span></h1>
        <p>Select from top AI models to compare their capabilities. Ask questions, generate content, or explore creative ideas.</p>
    </div>
    """, unsafe_allow_html=True)

# Display chat history
for i, (speaker, message_text) in enumerate(st.session_state.history):
    avatar = "U" if speaker == "user" else "AI"
    speaker_class = "user" if speaker == "user" else "ai"
    
    st.markdown(f"""
    <div class="message {speaker_class}">
        <div class="avatar">{avatar}</div>
        <div class="message-content">{message_text}</div>
    </div>
    """, unsafe_allow_html=True)

# Input container
st.markdown("""
<div class="input-container">
    <div class="input-box">
        <textarea 
            id="prompt" 
            class="chat-input" 
            placeholder="Message AI Explorer..." 
            rows="1"
        ></textarea>
        <button id="generate" class="send-btn">
            <i class="fas fa-paper-plane"></i>
        </button>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main div

# JavaScript handlers
st.markdown("""
<script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function() {
    const promptInput = document.getElementById('prompt');
    const generateBtn = document.getElementById('generate');
    const chatContainer = document.getElementById('chat-container');
    const clearChatBtn = document.getElementById('clear-chat');
    const modelStatus = document.getElementById('model-status');
    
    // Auto-resize textarea
    promptInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Send message on button click
    generateBtn.addEventListener('click', sendMessage);
    
    // Send message on Enter (without Shift)
    promptInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Clear chat button
    clearChatBtn.addEventListener('click', function() {
        // Streamlit method to clear session state
        window.parent.postMessage({
            type: 'streamlit:clearHistory'
        }, '*');
    });
    
    // Start new chat function
    function startNewChat() {
        promptInput.value = '';
        promptInput.style.height = 'auto';
        modelStatus.textContent = 'Ready';
    }
    
    // Function to add message to chat UI
    function addMessageToChat(text, sender) {
        const avatar = sender === 'user' ? 'U' : 'AI';
        const speakerClass = sender;
        
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', speakerClass);
        messageDiv.innerHTML = `
            <div class="avatar">${avatar}</div>
            <div class="message-content">${text}</div>
        `;
        
        chatContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // Function to send message
    async function sendMessage() {
        const message = promptInput.value.trim();
        if (!message) return;
        
        // Add user message to Streamlit
        window.parent.postMessage({
            type: 'streamlit:userMessage',
            message: message
        }, '*');
        
        promptInput.value = '';
        promptInput.style.height = 'auto';
        
        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        typingIndicator.innerHTML = `
            <div>AI is typing</div>
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;
        chatContainer.appendChild(typingIndicator);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        // Disable send button during processing
        generateBtn.disabled = true;
        modelStatus.textContent = 'Generating...';
        
        try {
            // Simulate AI response
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // Add AI response to Streamlit
            window.parent.postMessage({
                type: 'streamlit:aiResponse',
                message: "This is a simulated response. In a real implementation, you would connect to an AI API like OpenAI, Anthropic, or Hugging Face."
            }, '*');
            
        } finally {
            // Re-enable send button
            generateBtn.disabled = false;
            modelStatus.textContent = 'Ready';
        }
    }
});
</script>
""", unsafe_allow_html=True)

# Handle message processing
def process_message(sender, message):
    st.session_state.history.append((sender, message))
    st.rerun()

# Handle messages from JavaScript
def handle_messages():
    if st.experimental_get_query_params().get("message"):
        message = st.experimental_get_query_params()["message"][0]
        sender = st.experimental_get_query_params()["sender"][0]
        process_message(sender, message)

# Handle clear history
def clear_history():
    st.session_state.history = []
    st.rerun()

# Handle message types
if 'message_type' in st.experimental_get_query_params():
    msg_type = st.experimental_get_query_params()['message_type'][0]
    
    if msg_type == "userMessage":
        message = st.experimental_get_query_params()['message'][0]
        process_message("user", message)
    elif msg_type == "aiResponse":
        message = st.experimental_get_query_params()['message'][0]
        process_message("ai", message)
    elif msg_type == "clearHistory":
        clear_history()

# Add dummy element to trigger message handling
st.empty()
