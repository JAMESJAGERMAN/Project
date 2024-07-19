import requests
import json
import random

API_KEY = "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"
API_URL = "https://api.qroq.ai/v1/converse"

ALLOWED_TOPICS = ['recipe', 'ingredient', 'cooking', 'baking', 'food', 'cuisine']

def is_relevant_question(question):
    question_lower = question.lower()
    return any(topic in question_lower for topic in ALLOWED_TOPICS)

def get_response(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    data = {
        "model": "qroq-v1",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    
    response = None
    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data), timeout=10)
    except requests.exceptions.ReadTimeout as e:
        print(f"Read timeout: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection error: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Timeout error: {e}")
    
    if response and response.status_code == 200:
        return response.json()['messages'][-1]['content']
    else:
        return f"Error: {response.status_code}, {response.text}"

def main():
    print("Welcome to the QROQ Chatbot!")
    print("I'll respond to your questions about recipes, ingredients, cooking, baking, food, and cuisine.")
    
    while True:
        user_input = input("\nYour question (or 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            print("Thank you for chatting with me! Goodbye!")
            break
        
        if not is_relevant_question(user_input):
            print("\nSorry, I'm not sure what you're asking. Could you please rephrase your question?")
            continue
        
        response = get_response(user_input)
        print("\n", response)

if __name__ == "__main__":
    main()