const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('./recipes.db');

db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    ingredients TEXT,
    instructions TEXT,
    cuisine TEXT,
    dietary_info TEXT
  )`);

  db.run(`INSERT INTO recipes (name, ingredients, instructions, cuisine, dietary_info)
VALUES 
  ('Chicken Alfredo Pasta', 'fettuccine pasta, chicken breast, heavy cream, butter, garlic, parmesan cheese, salt, black pepper', 'Cook pasta; sauté chicken and garlic; add cream, butter, and cheese; toss together.', 'Italian', 'Contains dairy'),
  ('Beef Tacos', 'ground beef, taco seasoning, tortillas, lettuce, tomato, cheddar cheese, salsa, sour cream', 'Brown beef with taco seasoning; fill tortillas with beef and toppings.', 'Mexican', 'Gluten-free'),
  ('Caesar Salad', 'romaine lettuce, croutons, parmesan cheese, Caesar dressing', 'Toss lettuce with dressing; add croutons and cheese; serve chilled.', 'American', 'Vegetarian'),
  ('Thai Green Curry', 'chicken thighs, green curry paste, coconut milk, bell peppers, bamboo shoots, Thai basil, fish sauce', 'Cook chicken with curry paste; add coconut milk and vegetables; simmer until cooked through.', 'Thai', 'Contains dairy'),
  ('Chocolate Chip Cookies', 'butter, brown sugar, white sugar, eggs, vanilla extract, flour, baking soda, chocolate chips', 'Cream butter and sugars; mix in eggs and vanilla; add dry ingredients and chocolate chips; bake until golden brown.', 'American', 'Contains dairy'),
  ('Caprese Salad', 'tomatoes, fresh mozzarella, basil leaves, balsamic vinegar, olive oil, salt, black pepper', 'Slice tomatoes and mozzarella; arrange with basil leaves; drizzle with vinegar and oil; season with salt and pepper.', 'Italian', 'Vegetarian'),
  ('Sushi Rolls', 'sushi rice, nori sheets, fish (salmon/tuna), avocado, cucumber, soy sauce, wasabi, pickled ginger', 'Prepare sushi rice; place ingredients on nori; roll tightly and slice into pieces; serve with soy sauce, wasabi, and ginger.', 'Japanese', 'Gluten-free'),
  ('Mushroom Risotto', 'Arborio rice, mushrooms (shiitake/cremini), onion, garlic, vegetable broth, white wine, parmesan cheese, butter', 'Sauté mushrooms, onion, and garlic; add rice and cook with broth and wine; stir in cheese and butter.', 'Italian', 'Vegetarian'),
  ('Beef Stroganoff', 'beef sirloin, mushrooms, onion, garlic, beef broth, sour cream, Dijon mustard, egg noodles', 'Sear beef; sauté mushrooms, onion, and garlic; add broth, sour cream, and mustard; serve over noodles.', 'Russian', 'Contains dairy'),
  ('Greek Salad', 'cucumbers, tomatoes, red onion, kalamata olives, feta cheese, oregano, olive oil, red wine vinegar, salt, black pepper', 'Combine vegetables with olives and cheese; dress with oil, vinegar, and seasonings; serve chilled.', 'Greek', 'Vegetarian');
`);
});

db.close();
