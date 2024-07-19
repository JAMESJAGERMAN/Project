import requests
import spacy
import random
import json
from collections import Counter
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
            data = f.read()
            if data:
                return json.loads(data)
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
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

def suggest_recipe(user_input=None):
    history = load_search_history()
    
    if user_input:
        parsed_meal_name = parse_user_input(user_input)
        print(f"Searching for: '{parsed_meal_name}'")
        meals = search_meal_by_name(parsed_meal_name)
        display_meals(meals)
        if meals:
            add_to_search_history(parsed_meal_name)
    else:
        if not history:
            print("Your search history is empty. Here's a random recipe suggestion:")
            meals = get_random_meal()
            display_meals(meals)
        else:
            if random.random() < 0.3:  # 30% chance of random suggestion
                print("Here's a random recipe suggestion:")
                meals = get_random_meal()
                display_meals(meals)
            else:
                # Analyze search history
                meal_categories = []
                meal_areas = []
                meal_ingredients = []

                for record in history:
                    meal_name = record['meal']
                    meals = search_meal_by_name(meal_name)
                    if meals:
                        for meal in meals:
                            if meal.get('strCategory'):
                                meal_categories.append(meal['strCategory'])
                            if meal.get('strArea'):
                                meal_areas.append(meal['strArea'])
                            for i in range(1, 21):
                                ingredient = meal.get(f'strIngredient{i}')
                                if ingredient and ingredient.strip():
                                    meal_ingredients.append(ingredient)

                # Find most common categories, areas, and ingredients
                common_category = Counter(meal_categories).most_common(1)
                common_area = Counter(meal_areas).most_common(1)
                common_ingredient = Counter(meal_ingredients).most_common(1)

                print("Based on your search history, you might like recipes in these categories or with these ingredients:")
                if common_category:
                    print(f"Category: {common_category[0][0]}")
                if common_area:
                    print(f"Area: {common_area[0][0]}")
                if common_ingredient:
                    print(f"Ingredient: {common_ingredient[0][0]}")

                # Suggest a meal based on the most common attributes
                suggested_meals = []
                if common_category:
                    suggested_meals += search_meal_by_name(common_category[0][0]) or []
                if common_area:
                    suggested_meals += search_meal_by_name(common_area[0][0]) or []
                if common_ingredient:
                    suggested_meals += filter_meal_by_ingredient(common_ingredient[0][0]) or []

                # Remove duplicates
                unique_meals = {meal['idMeal']: meal for meal in suggested_meals}.values()
                display_meals(list(unique_meals))
                
                return unique_meals

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
            user_input = input("What kind of recipe are you looking for? (Press Enter to get a suggestion based on your search history): ")
            suggest_recipe(user_input)
        
        elif choice == "4":
            break
        
        else:   
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
