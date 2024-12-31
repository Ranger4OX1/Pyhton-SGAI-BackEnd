import streamlit as st
import sqlite3
import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"


# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            user_message TEXT,
            bot_response TEXT
        )
    """)
    conn.commit()
    conn.close()


# Fetch all chat sessions from the database
def fetch_all_sessions():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT chat_id FROM chat_history ORDER BY chat_id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]


# Fetch chat history for a specific chat ID
def fetch_chat_history(chat_id):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_message, bot_response FROM chat_history WHERE chat_id = ? ORDER BY id ASC", (chat_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


# Save a chat session to the database
def save_to_db(chat_id, user_message, bot_response):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (chat_id, user_message, bot_response) VALUES (?, ?, ?)",
                   (chat_id, user_message, bot_response))
    conn.commit()
    conn.close()


# Load system content from a file
def load_system_content(file_path="system_content.txt"):
    try:
        with open(file_path, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return "You are a helpful assistant."


# Initialize database
init_db()

# Sidebar for chat sessions
st.sidebar.title("📂 Chat Sessions")
session_ids = fetch_all_sessions()

# Option to start a new chat
if st.sidebar.button("➕ Start New Chat"):
    if session_ids:
        st.session_state.chat_id = max(session_ids) + 1
    else:
        st.session_state.chat_id = 1  # Start with chat_id 1 if no sessions exist
    st.session_state.chat_history = []
else:
    selected_chat_id = st.sidebar.selectbox("Select a Chat", session_ids)
    if selected_chat_id:
        st.session_state.chat_id = selected_chat_id
        st.session_state.chat_history = fetch_chat_history(selected_chat_id)

# Breadcrumb-like header
st.markdown(f"**Chat Session {st.session_state.chat_id if 'chat_id' in st.session_state else ''}**")

# Chat Interface
if "chat_id" in st.session_state:
    # Display chat history (oldest message first)
    st.write("---")
    chat_container = st.container()
    with chat_container:
        for idx, (user_message, bot_response) in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.markdown(f"{user_message}")
            with st.chat_message("assistant"):
                st.markdown(f"{bot_response}")

    # Auto-scroll to bottom by using a hidden placeholder
    st.markdown("<div id='scroll-to-bottom'></div>", unsafe_allow_html=True)
    st.markdown(
        "<script>document.getElementById('scroll-to-bottom').scrollIntoView({ behavior: 'smooth' });</script>",
        unsafe_allow_html=True,
    )

    # Message input fixed at the bottom
    st.write("---")
    col1, col2 = st.columns([5, 1])
    with col1:
        user_message = st.text_input("", key="user_message_input", placeholder="Type your message here...")
    with col2:
        send_button = st.button("Send")

    if send_button and user_message:
        # Load system content from file
        system_content = load_system_content()

        # Call the API
        payload = {
            "model": "llama3.2",
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_message}
            ],
            "stream": False
        }
        try:
            response = requests.post(OLLAMA_API_URL, json=payload)
            response.raise_for_status()
            bot_response = response.json().get("message", {}).get("content", "No response.")
        except Exception as e:
            bot_response = f"Error: {e}"

        # Update chat history and save to database
        st.session_state.chat_history.append((user_message, bot_response))
        save_to_db(st.session_state.chat_id, user_message, bot_response)
        st.rerun()

else:
    st.write("Start a new chat or select an existing session from the sidebar.")