import requests
import json

OLLAMA_API_URL = "http://localhost:11434/api/chat"

def chat_with_ollama(model, user_message):
    """
    Send a message to the Ollama API and return the complete response by setting stream to false.
    """
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": "you are a Data Analyst"},
                     {"role": "user", "content": user_message}],
        "stream": False  # Set stream to false to receive the full response in one go
    }
    
    try:
        # Send the request with stream set to false
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # Check for request errors
        
        # Parse the JSON response
        data = response.json()
        
        # Extract and return the content
        if "message" in data and "content" in data["message"]:
            return data["message"]["content"].strip()
        else:
            return "No content found in response."

    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama API: {e}"

# Example usage
# response = chat_with_ollama("llama2", "why is the sky blue?")
# print("Final Response:", response)


def main():
    print("Welcome to the Ollama CLI Chatbot!")
    print("Type 'exit' to end the chat.\n")

    # Define the model you want to use
    model_name = "llama2"  # Replace with your preferred model name

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        
        # Get the response from the model
        bot_response = chat_with_ollama(model_name, user_input)
        # print(bot_response)
        print(f"Bot: {bot_response}")

if __name__ == "__main__":
    main()
