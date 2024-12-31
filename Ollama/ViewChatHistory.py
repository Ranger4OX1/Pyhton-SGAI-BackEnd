import streamlit as st
import sqlite3
import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"

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

# Summarize messages using LLM
def summarize_message(message):
    payload = {
        "model": "llama3.2",
        "messages": [
            {"role": "system", "content": "Summarize the following conversation:"},
            {"role": "user", "content": message}
        ],
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        summary = response.json().get("message", {}).get("content", "No summary available.")
        return summary
    except Exception as e:
        return f"Error summarizing message: {e}"

# Streamlit UI to view chat history
st.title("Chat History Viewer")

# Sidebar for chat sessions
st.sidebar.title("Chat Sessions")
session_ids = fetch_all_sessions()

if not session_ids:
    st.sidebar.write("No sessions available.")
else:
    selected_chat_id = st.sidebar.selectbox("Select a Chat Session", session_ids)

    if selected_chat_id:
        st.write(f"### Chat History for Session {selected_chat_id}")

        # Fetch chat history for the selected session
        chat_history = fetch_chat_history(selected_chat_id)
        table_data = []
        for user_message, bot_response in chat_history:
            full_message = f"User: {user_message}\nBot: {bot_response}"
            summary = summarize_message(full_message)
            table_data.append((user_message, bot_response, summary))

        for idx, (user_message, bot_response, summary) in enumerate(table_data):
            st.markdown(f"**Message {idx + 1}:** {summary}")
            if st.button(f"Show Full Message {idx + 1}", key=f"show_{idx}"):
                st.markdown(f"""
                **User**: {user_message}  
                **Bot**: {bot_response}  
                """, unsafe_allow_html=True)
            st.markdown("---")
