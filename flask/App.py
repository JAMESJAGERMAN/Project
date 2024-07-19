from flask import Flask, redirect, render_template, request, url_for
import requests
import spacy
import random
import json
from collections import Counter
from datetime import datetime
app = Flask(__name__)

if __name__ == '__Main__':
    app.run(debug=True, port=5000)


# Constants
BASE_URL = "https://www.themealdb.com/api/json/v1/1/"
HISTORY_FILE = "search_history.json"
nlp = spacy.load("en_core_web_sm")

def search_meal_by_name(meal_name):
    url = f"{BASE_URL}search.php?s={meal_name}"
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

def suggest_recipe(user_input=None):
    history = load_search_history()
    
    if user_input:
        parsed_meal_name = parse_user_input(user_input)
        meals = search_meal_by_name(parsed_meal_name)
        if meals:
            add_to_search_history(parsed_meal_name)
        return meals
    else:
        if not history:
            return get_random_meal()
        else:
            if random.random() < 0.3:  # 30% chance of random suggestion
                return get_random_meal()
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

                suggested_meals = []
                if common_category:
                    suggested_meals += search_meal_by_name(common_category[0][0]) or []
                if common_area:
                    suggested_meals += search_meal_by_name(common_area[0][0]) or []
                if common_ingredient:
                    suggested_meals += filter_meal_by_ingredient(common_ingredient[0][0]) or []

                unique_meals = {meal['idMeal']: meal for meal in suggested_meals}.values()
                return list(unique_meals)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    user_input = request.form.get('user_input')
    if not user_input:
        return redirect(url_for('index'))
    
    meals = suggest_recipe(user_input)
    return render_template('results.html', meals=meals)

if __name__ == "__main__":
    app.run(debug=True)