import requests
import spacy

BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def search_meal_by_name(meal_name):
    url = f"{BASE_URL}search.php?s={meal_name}"
    print(f"Searching URL: {url}")  # Debug print
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['meals']
    else:
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
            print(f"Instructions: {meal.get('strInstructions', 'N/A')}")
            print(f"Image: {meal.get('strMealThumb', 'N/A')}")
            print("-" * 40)
    else:
        print("No meals found.")

def parse_user_input(user_input):
    doc = nlp(user_input.lower())
    
    # Extract nouns and adjectives as potential meal names
    meal_words = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]
    
    # Join the extracted words
    meal_name = ' '.join(meal_words)
    
    return meal_name.strip()

def main():
    while True:
        print("\nMenu:")
        print("1. Search for a recipe")
        print("2. Filter meal by ingredient")
        print("3. Exit")
        
        choice = input("Enter your choice or ask for a recipe: ")
        
        if choice == "1" or "recipe" in choice.lower() or "how to make" in choice.lower():
            if choice == "1":
                meal_name = input("Enter meal name or ask for a recipe: ")
            else:
                meal_name = choice
            
            parsed_meal_name = parse_user_input(meal_name)
            print(f"Searching for: '{parsed_meal_name}'")  # Debug print
            meals = search_meal_by_name(parsed_meal_name)
            display_meals(meals)
        
        elif choice == "2":
            ingredient = input("Enter ingredient: ")
            meals = filter_meal_by_ingredient(ingredient)
            display_meals(meals)
        
        elif choice == "3":
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()