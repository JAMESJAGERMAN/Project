import json

API_KEY = "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"

ALLOWED_TOPICS = ['recipe', 'ingredient', 'cooking', 'baking', 'food', 'cuisine']

def is_relevant_question(question):
    question_lower = question.lower()
    return any(topic in question_lower for topic in ALLOWED_TOPICS)

def process_request(messages, model):
    # This is a placeholder function. In a real scenario, you would implement
    # your own logic here to process the request and generate a response.
    # For demonstration purposes, we'll just return a simple response.
    user_message = messages[-1]['content']
    return f"Here's a recipe response for: {user_message}"

def get_recipe_response(prompt):
    system_message = """
    You are a specialized AI assistant focused solely on recipes, ingredients, and cooking.
    Only answer questions directly related to these topics. If a question is not about
    recipes, ingredients, or cooking, politely explain that you can only assist with
    cooking-related queries. Do not provide any information outside of this scope.
    """
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    model = "mixtral-8x7b-32768"  # or another appropriate model
    
    response = process_request(messages, model)
    return response

def main():
    print("Welcome to the AI Recipe Recommendation App!")
    print("Ask me about recipes, ingredients, or cooking assistance.")
    
    while True:
        user_input = input("\nYour question (or 'quit' to exit): ")
        
        if user_input.lower() == 'quit':
            print("Thank you for using the AI Recipe Recommendation App. Goodbye!")
            break
        
        if not is_relevant_question(user_input):
            print("\nAI Assistant: I'm sorry, but I can only answer questions about recipes, ingredients, and cooking. Could you please ask a cooking-related question?")
            continue
        
        response = get_recipe_response(user_input)
        print("\nAI Assistant:", response)

if __name__ == "__main__":
    main()