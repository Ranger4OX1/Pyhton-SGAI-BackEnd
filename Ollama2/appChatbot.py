from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
import requests

OLLAMA_API_URL = "http://localhost:11434/api/chat"

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/')
def home():
    return render_template('index.html')  # Serve the index.html file


def chat_with_ollama(model, user_message):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "you are a Data Analyst"},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        if "message" in data and "content" in data["message"]:
            return data["message"]["content"].strip()
        else:
            return "No content found in response."
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama API: {e}"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if "message" not in data:
        return jsonify({"error": "No message provided"}), 400

    user_message = data["message"]
    # model_name = "llama2"  # You can change the model name here
    model_name = "llama3.2"  # You can change the model name here
    response = chat_with_ollama(model_name, user_message)

    return jsonify({"reply": response})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
