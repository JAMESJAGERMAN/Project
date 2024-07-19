import requests
import spacy
import random
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from tkinter import Tk, Canvas, Entry, scrolledtext, PhotoImage, messagebox, font

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
    text_widget.delete(1.0, "end")
    if meals:
        for meal in meals:
            text_widget.insert("end", f"Name: {meal.get('strMeal', 'N/A')}\n")
            text_widget.insert("end", f"Category: {meal.get('strCategory', 'N/A')}\n")
            text_widget.insert("end", f"Area: {meal.get('strArea', 'N/A')}\n")
            
            text_widget.insert("end", "\nIngredients:\n")
            for i in range(1, 21):
                ingredient = meal.get(f'strIngredient{i}')
                measure = meal.get(f'strMeasure{i}')
                if ingredient and ingredient.strip():
                    text_widget.insert("end", f"- {measure} {ingredient}\n")
            
            text_widget.insert("end", "\nInstructions:\n")
            text_widget.insert("end", f"{meal.get('strInstructions', 'N/A')}\n")
            
            image_url = meal.get('strMealThumb', 'N/A')
            if image_url and image_url.strip():
                text_widget.insert("end", f"Image URL: {image_url}\n")
            
            text_widget.insert("end", "-" * 40 + "\n")
    else:
        text_widget.insert("end", "No meals found.\n")

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
            text_widget.insert("end", "Your search history is empty. Here's a random recipe suggestion:\n")
            meals = get_random_meal()
            display_meals(meals, text_widget)
        else:
            if random.random() < 0.3:  # 30% chance of random suggestion
                text_widget.insert("end", "Here's a random recipe suggestion:\n")
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

                text_widget.insert("end", "Based on your search history, you might like recipes in these categories or with these ingredients:\n")
                if common_category:
                    text_widget.insert("end", f"Category: {common_category[0][0]}\n")
                if common_area:
                    text_widget.insert("end", f"Area: {common_area[0][0]}\n")
                if common_ingredient:
                    text_widget.insert("end", f"Ingredient: {common_ingredient[0][0]}\n")

                suggested_meals = []
                if common_category:
                    suggested_meals += search_meal_by_name(common_category[0][0]) or []
                if common_area:
                    suggested_meals += search_meal_by_name(common_area[0][0]) or []
                if common_ingredient:
                    suggested_meals += filter_meal_by_ingredient(common_ingredient[0][0]) or []

                unique_meals = {meal['idMeal']: meal for meal in suggested_meals}.values()
                display_meals(list(unique_meals), text_widget)

def search_recipe(event):
    results_text.place(x=201.0, y=200.0, width=877.0, height=400.0)
    meal_name = parse_user_input(entry_1.get())
    meals = search_meal_by_name(meal_name)
    display_meals(meals, results_text)
    if meals:
        add_to_search_history(meal_name)

def filter_recipe(event):
    results_text.place(x=201.0, y=200.0, width=877.0, height=400.0)
    ingredient = entry_1.get()
    meals = filter_meal_by_ingredient(ingredient)
    display_meals(meals, results_text)

def suggest_recipe_gui(event):
    results_text.place(x=201.0, y=200.0, width=877.0, height=400.0)
    suggest_recipe(None, results_text)

# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Rakaputu Banardi A\Documents\AI class\AI Project\GUI\build\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("1282x740")
window.configure(bg = "#FFFFFF")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 740,
    width = 1282,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    641.0,
    370.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    638.0,
    156.0,
    image=image_image_2
)

canvas.create_text(
    525.0,
    10.0,
    anchor="nw",
    text="AI-Powered Recipe",
    fill="#000000",
    font=("BonaNova Regular", 30 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    639.5,
    155.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFF3DB",
    fg="#000716",
    highlightthickness=0,
    font=("Bonheur Royale", 16)
)
entry_1.place(
    x=201.0,
    y=123.0,
    width=877.0,
    height=62.0
)

entry_1.bind("<Return>", search_recipe)

results_text = scrolledtext.ScrolledText(window, width=80, height=20, wrap="word", font=("Bonheur Royale", 14))
results_text.place_forget()

window.resizable(False, False)
window.mainloop()
