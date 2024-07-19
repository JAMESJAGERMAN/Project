import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [ingredients, setIngredients] = useState('');
  const [recipes, setRecipes] = useState([]);

  const fetchRecipes = () => {
    axios.post('http://localhost:3000/ingredients', {
      ingredients: ingredients.split(','),
    })
    .then(response => {
      setRecipes(response.data);
    })
    .catch(error => {
      console.error('There was an error fetching the recipes!', error);
    });
  };

  return (
    <div>
      <h1>Recipe Recommendation App</h1>
      <input
        type="text"
        value={ingredients}
        onChange={e => setIngredients(e.target.value)}
        placeholder="Enter ingredients separated by commas"
      />
      <button onClick={fetchRecipes}>Get Recipes</button>
      <ul>
        {recipes.map(recipe => (
          <li key={recipe.id}>
            <h2>{recipe.name}</h2>
            <p><strong>Ingredients:</strong> {recipe.ingredients}</p>
            <p><strong>Instructions:</strong> {recipe.instructions}</p>
            <p><strong>Cuisine:</strong> {recipe.cuisine}</p>
            <p><strong>Dietary Info:</strong> {recipe.dietary_info}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
