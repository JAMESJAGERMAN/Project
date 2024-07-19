import requests
import spacy
import random
import json
from datetime import datetime

BASE_URL = "https://www.themealdb.com/api/json/v1/1/"
HISTORY_FILE = "search_history.json"

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def search_meal_by_name(meal_name):
    url = f"{BASE_URL}search.php?s={meal_name}"
    print(f"Searching URL: {url}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['meals']
    else:
        print(f"API request failed with status code: {response.status_code}")
        return None

def filter_meal_by_ingredient(ingredient):
    url = f"{BASE_URL}filter.php?i={ingredient}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['meals']
    else:
        return None

def display_meals(meals):
    if meals:
        for meal in meals:
            print(f"Name: {meal.get('strMeal', 'N/A')}")
            print(f"Category: {meal.get('strCategory', 'N/A')}")
            print(f"Area: {meal.get('strArea', 'N/A')}")
            
            print("\nIngredients:")
            for i in range(1, 21):
                ingredient = meal.get(f'strIngredient{i}')
                measure = meal.get(f'strMeasure{i}')
                if ingredient and ingredient.strip():
                    print(f"- {measure} {ingredient}")
            
            print("\nInstructions:")
            print(meal.get('strInstructions', 'N/A'))
            
            print(f"\nImage: {meal.get('strMealThumb', 'N/A')}")
            print("-" * 40)
    else:
        print("No meals found.")

def parse_user_input(user_input):
    stop_words = {"recipe", "for", "how", "to", "make"}
    doc = nlp(user_input.lower())
    meal_words = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and token.text not in stop_words]
    meal_name = ' '.join(meal_words)
    print(f"Original input: '{user_input}'")
    print(f"Parsed meal name: '{meal_name}'")
    return meal_name.strip()

def load_search_history():
    try:
        with open(HISTORY_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_search_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def add_to_search_history(meal_name):
    history = load_search_history()
    history.append({"meal": meal_name, "date": datetime.now().isoformat()})
    save_search_history(history)

def get_random_meal():
    url = f"{BASE_URL}random.php"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['meals']
    else:
        return None

def suggest_recipe():
    history = load_search_history()
    if not history or random.random() < 0.3:  # 30% chance of random suggestion
        print("Here's a random recipe suggestion:")
        return get_random_meal()
    else:
        recent_searches = [item['meal'] for item in history[-5:]]  # Get last 5 searches
        suggested_meal = random.choice(recent_searches)
        print(f"Based on your recent searches, how about trying {suggested_meal}?")
        return search_meal_by_name(suggested_meal)

def main():
    while True:
        print("\nMenu:")
        print("1. Search for a recipe")
        print("2. Filter meal by ingredient")
        print("3. Get a suggestion")
        print("4. Exit")
        
        choice = input("Enter your choice or ask for a recipe: ")
        
        if choice == "1" or "recipe" in choice.lower() or "how to make" in choice.lower():
            if choice == "1":
                meal_name = input("Enter meal name or ask for a recipe: ")
            else:
                meal_name = choice
            
            parsed_meal_name = parse_user_input(meal_name)
            print(f"Searching for: '{parsed_meal_name}'")
            meals = search_meal_by_name(parsed_meal_name)
            display_meals(meals)
            if meals:
                add_to_search_history(parsed_meal_name)
        
        elif choice == "2":
            ingredient = input("Enter ingredient: ")
            meals = filter_meal_by_ingredient(ingredient)
            display_meals(meals)
        
        elif choice == "3" or "suggest" in choice.lower() or "bored" in choice.lower():
            meals = suggest_recipe()
            display_meals(meals)
        
        elif choice == "4":
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
