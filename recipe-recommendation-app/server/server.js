const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();

const app = express();
app.use(cors());
app.use(bodyParser.json());

const db = new sqlite3.Database('./db/recipes.db');

app.get('/recipes', (req, res) => {
  db.all('SELECT * FROM recipes', [], (err, rows) => {
    if (err) {
      res.status(400).json({ error: err.message });
      return;
    }
    res.json(rows);
  });
});

app.post('/ingredients', (req, res) => {
  const userIngredients = req.body.ingredients;
  db.all('SELECT * FROM recipes', [], (err, rows) => {
    if (err) {
      res.status(400).json({ error: err.message });
      return;
    }

    const recommendedRecipes = rows.filter(recipe => {
      const recipeIngredients = recipe.ingredients.split(',');
      return userIngredients.every(ingredient =>
        recipeIngredients.includes(ingredient.trim())
      );
    });

    res.json(recommendedRecipes);
  });
});

app.listen(3000, () => console.log('Server running on port 3000'));
