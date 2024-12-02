import requests

# Configure your Ollama API endpoint
OLLAMA_API_URL = "http://127.0.0.1:11434/api/chat"  # Replace with your API URL if hosted elsewhere

def chat_with_ollama(model, user_message):
    """
    Send a message to the Ollama API and return the response.
    """
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": "you are a salty pirate"},
                     {"role": "user", "content": user_message}]
    }
    
    try:
        print(payload)
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()  # Raise an error for HTTP issues
        print("Raw Response Text:", response.text)  # Debug: Print the raw response

        # Parse JSON and extract the content
        data = response.json()
        # Extracting the assistant's response from the "message" key
        return data["message"]["content"].strip() if "message" in data else "No response content received."
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama API: {e}"
    except ValueError as ve:
        return f"Error parsing JSON response: {ve}"


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
        print(bot_response)
        print(f"Bot: {bot_response}")

if __name__ == "__main__":
    main()
