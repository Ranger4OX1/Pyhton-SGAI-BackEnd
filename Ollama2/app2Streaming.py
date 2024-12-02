import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/chat"

def chat_with_ollama(model, user_message):
    """
    Send a message to the Ollama API and handle streaming JSON responses.
    """
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": "you are a salty pirate"},
                     {"role": "user", "content": user_message}]
    }
    
    try:
        # Open the request with streaming enabled
        response = requests.post(OLLAMA_API_URL, json=payload, stream=True)
        response.raise_for_status()
        
        # Parse the streaming response
        final_content = ""
        for line in response.iter_lines():
            if line:  # Avoid empty lines
                try:
                    data = json.loads(line.decode('utf-8'))  # Decode and parse each line
                    if "message" in data and "content" in data["message"]:
                        final_content += data["message"]["content"]
                except json.JSONDecodeError:
                    # Log or handle malformed JSON if needed
                    print(f"Malformed JSON line: {line}")
        
        return final_content.strip() if final_content else "No response content received."
    
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama API: {e}"

# Example usage
response = chat_with_ollama("llama2", "why is the sky blue?")
print("Final Response:", response)
