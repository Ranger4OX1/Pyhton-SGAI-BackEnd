import streamlit as st
import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"

# Initialize session state
if "user_message_input" not in st.session_state:
    st.session_state.user_message_input = ""

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "system_role_content" not in st.session_state:
    st.session_state.system_role_content = "you are a Data Analyst"  # Default role

# Function to adjust height based on text length
def calculate_height(text, line_height=20, min_height=100, max_height=300):
    lines = text.count('\n') + 1
    estimated_height = min(max(lines * line_height, min_height), max_height)
    return estimated_height

# Function to send a message to the API
def send_message():
    user_message = st.session_state.user_message_input
    if not user_message:
        return

    # Call the API
    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "system", "content": st.session_state.system_role_content},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        reply = response.json().get("message", {}).get("content", "No response.")
    except Exception as e:
        reply = f"Error: {e}"

    # Add the conversation to chat history
    st.session_state.chat_history.insert(0, {"user": user_message, "bot": reply})
    st.session_state.user_message_input = ""  # Reset input field

# Sidebar for system role customization and Save button
with st.sidebar:
    st.header("System Role Settings")
    height = calculate_height(st.session_state.system_role_content)
    # Directly update session state from text_area before button action
    new_system_role_content = st.text_area(
        "Enter System Role Content:",
        value=st.session_state.system_role_content,
        key="system_role_content",
        height=height,
        help="Change the system's role here."
    )
    if new_system_role_content != st.session_state.system_role_content:
        st.session_state.system_role_content = new_system_role_content
        st.success("System Role Content saved!")

# Main Chat UI
st.title("Chat with Ollama")

# Input message from the user
st.text_input("Type your message:", key="user_message_input", on_change=send_message)

# Display chat history with styling
st.write("### Chat History:")

for chat in st.session_state.chat_history:
    st.markdown(f"""
    <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; text-align: right;">
        <strong>You:</strong> {chat['user']}
    </div>
    <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px; color:pink background-color: #f9f9f9;">
        <strong>Bot:</strong> {chat['bot']}
    </div>
    <div>---------------------------------------------------------------------------------------------------------------------------------------------</div>
    """, unsafe_allow_html=True)
