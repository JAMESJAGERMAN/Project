import requests
import spacy
import random
import json
from collections import Counter
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

BASE_URL = "https://www.themealdb.com/api/json/v1/1/"
HISTORY_FILE = "search_history.json"

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

def search_meal_by_name(meal_name):
    url = f"{BASE_URL}search.php?s={meal_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['meals']
    else:
        messagebox.showerror("Error", f"API request failed with status code: {response.status_code}")
        return None

def filter_meal_by_ingredient(ingredient):
    url = f"{BASE_URL}filter.php?i={ingredient}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['meals']
    else:
        return None

def display_meals(meals, text_widget):
    text_widget.delete(1.0, tk.END)
    if meals:
        for meal in meals:
            text_widget.insert(tk.END, f"Name: {meal.get('strMeal', 'N/A')}\n")
            text_widget.insert(tk.END, f"Category: {meal.get('strCategory', 'N/A')}\n")
            text_widget.insert(tk.END, f"Area: {meal.get('strArea', 'N/A')}\n")
            
            text_widget.insert(tk.END, "\nIngredients:\n")
            for i in range(1, 21):
                ingredient = meal.get(f'strIngredient{i}')
                measure = meal.get(f'strMeasure{i}')
                if ingredient and ingredient.strip():
                    text_widget.insert(tk.END, f"- {measure} {ingredient}\n")
            
            text_widget.insert(tk.END, "\nInstructions:\n")
            text_widget.insert(tk.END, f"{meal.get('strInstructions', 'N/A')}\n")
            
            text_widget.insert(tk.END, f"\nImage: {meal.get('strMealThumb', 'N/A')}\n")
            text_widget.insert(tk.END, "-" * 40 + "\n")
    else:
        text_widget.insert(tk.END, "No meals found.\n")

def parse_user_input(user_input):
    stop_words = {"recipe", "for", "how", "to", "make"}
    doc = nlp(user_input.lower())
    meal_words = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN'] and token.text not in stop_words]
    meal_name = ' '.join(meal_words)
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

def suggest_recipe(user_input=None, text_widget=None):
    history = load_search_history()
    
    if user_input:
        parsed_meal_name = parse_user_input(user_input)
        meals = search_meal_by_name(parsed_meal_name)
        display_meals(meals, text_widget)
        if meals:
            add_to_search_history(parsed_meal_name)
    else:
        if not history:
            text_widget.insert(tk.END, "Your search history is empty. Here's a random recipe suggestion:\n")
            meals = get_random_meal()
            display_meals(meals, text_widget)
        else:
            if random.random() < 0.3:  # 30% chance of random suggestion
                text_widget.insert(tk.END, "Here's a random recipe suggestion:\n")
                meals = get_random_meal()
                display_meals(meals, text_widget)
            else:
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

                common_category = Counter(meal_categories).most_common(1)
                common_area = Counter(meal_areas).most_common(1)
                common_ingredient = Counter(meal_ingredients).most_common(1)

                text_widget.insert(tk.END, "Based on your search history, you might like recipes in these categories or with these ingredients:\n")
                if common_category:
                    text_widget.insert(tk.END, f"Category: {common_category[0][0]}\n")
                if common_area:
                    text_widget.insert(tk.END, f"Area: {common_area[0][0]}\n")
                if common_ingredient:
                    text_widget.insert(tk.END, f"Ingredient: {common_ingredient[0][0]}\n")

                suggested_meals = []
                if common_category:
                    suggested_meals += search_meal_by_name(common_category[0][0]) or []
                if common_area:
                    suggested_meals += search_meal_by_name(common_area[0][0]) or []
                if common_ingredient:
                    suggested_meals += filter_meal_by_ingredient(common_ingredient[0][0]) or []

                unique_meals = {meal['idMeal']: meal for meal in suggested_meals}.values()
                display_meals(list(unique_meals), text_widget)

def search_recipe():
    meal_name = parse_user_input(search_entry.get())
    meals = search_meal_by_name(meal_name)
    display_meals(meals, results_text)
    if meals:
        add_to_search_history(meal_name)

def filter_recipe():
    ingredient = ingredient_entry.get()
    meals = filter_meal_by_ingredient(ingredient)
    display_meals(meals, results_text)

def suggest_recipe_gui():
    suggest_recipe(None, results_text)

app = tk.Tk()
app.title("Recipe Finder")

ttk.Label(app, text="Search for a Recipe:").grid(column=0, row=0, padx=10, pady=5, sticky="w")
search_entry = ttk.Entry(app, width=50)
search_entry.grid(column=1, row=0, padx=10, pady=5, sticky="w")
search_button = ttk.Button(app, text="Search", command=search_recipe)
search_button.grid(column=2, row=0, padx=10, pady=5)

ttk.Label(app, text="Filter by Ingredient:").grid(column=0, row=1, padx=10, pady=5, sticky="w")
ingredient_entry = ttk.Entry(app, width=50)
ingredient_entry.grid(column=1, row=1, padx=10, pady=5, sticky="w")
filter_button = ttk.Button(app, text="Filter", command=filter_recipe)
filter_button.grid(column=2, row=1, padx=10, pady=5)

suggest_button = ttk.Button(app, text="Suggest a Recipe", command=suggest_recipe_gui)
suggest_button.grid(column=1, row=2, padx=10, pady=5)

results_text = scrolledtext.ScrolledText(app, width=80, height=20, wrap=tk.WORD)
results_text.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

app.mainloop()
