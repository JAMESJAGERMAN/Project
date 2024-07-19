import requests

BASE_URL = "https://www.themealdb.com/api/json/v1/1/"

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

def main():
    while True:
        print("Menu:")
        print("1. Search meal by name")
        print("2. Filter meal by ingredient")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            meal_name = input("Enter meal name: ")
            meals = search_meal_by_name(meal_name)
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
