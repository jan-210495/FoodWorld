# resources/recipe_routes.py

# ------------------------------
# Imports
# ------------------------------

from flask import Blueprint, request, render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required
from utils.ai_helper import query_gemini, get_food_image, convert_lists_to_checkboxes
from bs4 import BeautifulSoup
import re
from dotenv import load_dotenv
import os
from models.recipe import Recipe
from models.category import Category
from models import db
from werkzeug.utils import secure_filename
import html

# ------------------------------
# Load environment variables
# ------------------------------

load_dotenv('appconfig.env')

# ------------------------------
# Define Blueprint
# ------------------------------

recipe_bp = Blueprint('recipe_bp', __name__, url_prefix='/recipes')

# ------------------------------
# Route: Recommend a recipe
# ------------------------------


@recipe_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.form
    ingredients = data.get('ingredients')
    servings = data.get('servings')

    prompt = f"""
    Suggest 3 recipes using these ingredients: {ingredients}. The meal should serve {servings} people.

    For each recipe, return HTML like this:

    <h3>Recipe Title</h3>
    <img src="image_url.jpg" alt="Recipe Title">
    <h4>Ingredients</h4>
    <ul>
      <li>ingredient 1</li>
      <li>ingredient 2</li>
    </ul>
    <h4>Instructions</h4>
    <ol>
      <li>step 1</li>
      <li>step 2</li>
    </ol>

    IMPORTANT: Do NOT wrap the HTML in triple backticks or code fences like ```html. Return pure HTML only.
    """

    ai_response = query_gemini(prompt)

    if ai_response:
        ai_response = html.unescape(ai_response)
        ai_response = re.sub(r"^```html\s*", "", ai_response)
        ai_response = re.sub(r"```$", "", ai_response)

        soup = BeautifulSoup(ai_response, "html.parser")

        # Replace placeholder images
        for img in soup.find_all("img"):
            alt_text = img.get("alt", "")
            new_img_url = get_food_image(alt_text)
            img["src"] = new_img_url

        # Convert lists to checkboxes
        soup = convert_lists_to_checkboxes(soup)

        html_result = str(soup)

        return render_template("search_results.html", result=html_result)

    else:
        return render_template("search_results.html",
                               result="No suggestions found.")

# ------------------------------
# Route: Substitute an Ingredient
# ------------------------------


@recipe_bp.route('/recommend/substitute', methods=['POST'])
def recommend_substitute():
    data = request.get_json()
    print("Received data:", data)

    if data is None:
        return jsonify({"suggestion": "No data received!"})

    missing_ingredient = data.get("missing_ingredient")
    recipe_name = data.get("recipe_name", "")

    print("Missing ingredient:", missing_ingredient)
    print("Recipe name:", recipe_name)

    prompt = f"""
    A user is missing the ingredient: {missing_ingredient}.
    {'They are cooking ' + recipe_name + '.' if recipe_name else ''}
    Suggest one or more substitute ingredients the user can use instead.
    Keep the answer short and user-friendly.
    """

    print("Prompt:", prompt)

    ai_response = query_gemini(prompt)

    print("AI response:", ai_response)

    if ai_response:
        suggestion = html.unescape(ai_response.strip())
        return jsonify({"suggestion": suggestion})
    else:
        return jsonify({"suggestion": "Sorry, I couldn't find a substitute this time."})



# ------------------------------
# Route: Show all recipes
# ------------------------------


@recipe_bp.route('/', methods=['GET'])
def cards_page():
    """
    Displays all recipes or recipes filtered by category.
    """
    category_id = request.args.get('category_id', type=int)

    if category_id:
        recipes = Recipe.query.filter_by(category_id=category_id).all()
    else:
        recipes = Recipe.query.all()

    return render_template("cards.html", recipes=recipes)


# ------------------------------
# Route: Show single recipe details
# ------------------------------


@recipe_bp.route('/<int:recipe_id>')
def recipe_detail(recipe_id):
    """
    Displays details of a single recipe.
    """
    recipe = Recipe.query.get_or_404(recipe_id)
    return render_template('recipe.html', recipe=recipe)


# ------------------------------
# Route: Admin Dashboard
# ------------------------------


@recipe_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    Admin-only dashboard displaying all recipes in a table.
    """
    if current_user.role != 'admin':
        return redirect(url_for('user_bp.home'))

    recipes = Recipe.query.all()
    return render_template('dashboard.html', recipes=recipes)


# ------------------------------
# Route: Add new recipe
# ------------------------------


@recipe_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    """
    Allows an admin to add a new recipe.
    """
    if current_user.role != 'admin':
        return redirect(url_for('user_bp.home'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        ingredients = request.form.get('ingredients')
        category = request.form.get('category')

        # Handle image upload
        photo_file = request.files.get('photo')
        photo_url = None

        if photo_file and photo_file.filename:
            filename = secure_filename(photo_file.filename)
            upload_path = os.path.join('static', 'uploads', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            photo_file.save(upload_path)
            photo_url = f"/static/uploads/{filename}"

        recipe = Recipe(name=name,
                        description=description,
                        ingredients=ingredients,
                        category=category,
                        photo=photo_url)

        db.session.add(recipe)
        db.session.commit()
        return redirect(url_for('recipe_bp.dashboard'))

    return render_template('add_recipe.html')


# ------------------------------
# Route: Edit existing recipe
# ------------------------------


@recipe_bp.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    """
    Allows the admin to edit an existing recipe.
    """
    if current_user.role != 'admin':
        return redirect(url_for('user_bp.home'))

    recipe = Recipe.query.get_or_404(recipe_id)

    if request.method == 'POST':
        recipe.name = request.form.get('name')
        recipe.description = request.form.get('description')
        recipe.ingredients = request.form.get('ingredients')
        recipe.category = request.form.get('category')
        recipe.photo = request.form.get('photo')
        db.session.commit()
        return redirect(url_for('recipe_bp.dashboard'))

    return render_template('edit_recipe.html', recipe=recipe)


# ------------------------------
# Route: Delete existing recipe
# ------------------------------


@recipe_bp.route('/delete/<int:recipe_id>', methods=['POST'])
@login_required
def delete_recipe(recipe_id):
    """
    Allows the admin to delete an existing recipe.
    """
    if current_user.role != 'admin':
        return redirect(url_for('user_bp.home'))

    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('recipe_bp.dashboard'))


# ------------------------------
# Route: List all categories
# ------------------------------


@recipe_bp.route('/categories')
def list_categories():
    """
    Displays all recipe categories.
    """
    categories = Category.query.all()
    return render_template("categories.html", categories=categories)


# ------------------------------
# Route: Show recipes by category
# ------------------------------


@recipe_bp.route('/category/<int:category_id>')
def recipes_by_category(category_id):
    """
    Displays recipes filtered by a specific category.
    """
    category = Category.query.get_or_404(category_id)
    recipes = Recipe.query.filter_by(category_id=category.id).all()
    return render_template("cards.html", recipes=recipes, category=category)


# ------------------------------
# Route: Search recipes
# ------------------------------


@recipe_bp.route('/search')
def search_recipes():
    """
    Search recipes by name.
    """
    query = request.args.get("q", "")
    if query:
        results = Recipe.query.filter(Recipe.name.ilike(f"%{query}%")).all()
    else:
        results = []
    return render_template("search_results.html", recipes=results, query=query)
