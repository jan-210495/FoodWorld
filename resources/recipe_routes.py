# resources/recipe_routes.py

# ------------------------------
# Imports
# ------------------------------

from flask import Blueprint, flash, request, render_template, redirect, url_for, jsonify
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from utils.ai_helper import query_gemini, get_food_image, convert_lists_to_checkboxes
from utils.validation import validate_recipe_form
from bs4 import BeautifulSoup
import re
from models.recipe import Recipe
from models.category import Category
from models import db
import html

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
        return jsonify(
            {"suggestion": "Sorry, I couldn't find a substitute this time."})


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
    """Allow an administrator to add a recipe from an existing category."""
    if current_user.role != 'admin':
        return redirect(url_for('user_bp.home'))

    categories = Category.query.order_by(Category.name).all()

    if request.method == 'POST':
        recipe_data, errors = validate_recipe_form(request.form)

        if not errors:
            category = db.session.get(Category, recipe_data['category_id'])
            if category is None:
                errors.append("The selected category does not exist.")

        if not errors:
            duplicate = Recipe.query.filter(
                Recipe.name.ilike(recipe_data['name'])
            ).first()
            if duplicate:
                errors.append("A recipe with this name already exists.")

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template(
                'add_recipe.html',
                categories=categories,
                form_data=request.form,
            ), 400

        recipe = Recipe(
            name=recipe_data['name'],
            description=recipe_data['description'],
            ingredients=recipe_data['ingredients'],
            instructions=recipe_data['instructions'],
            photo=recipe_data['photo'],
            category_id=recipe_data['category_id'],
        )

        try:
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("The recipe could not be saved. Please try again.", 'error')
            return render_template(
                'add_recipe.html',
                categories=categories,
                form_data=request.form,
            ), 409

        flash("Recipe added successfully.", 'success')
        return redirect(url_for('recipe_bp.dashboard'))

    return render_template('add_recipe.html', categories=categories, form_data={})


# ------------------------------
# Route: Edit existing recipe
# ------------------------------


@recipe_bp.route('/edit/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    """Allow an administrator to edit an existing recipe."""
    if current_user.role != 'admin':
        return redirect(url_for('user_bp.home'))

    recipe = Recipe.query.get_or_404(recipe_id)
    categories = Category.query.order_by(Category.name).all()

    if request.method == 'POST':
        recipe_data, errors = validate_recipe_form(request.form)

        if not errors:
            category = db.session.get(Category, recipe_data['category_id'])
            if category is None:
                errors.append("The selected category does not exist.")

        if not errors:
            duplicate = Recipe.query.filter(
                Recipe.name.ilike(recipe_data['name']),
                Recipe.id != recipe.id,
            ).first()
            if duplicate:
                errors.append("A recipe with this name already exists.")

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template(
                'edit_recipe.html',
                recipe=recipe,
                categories=categories,
                form_data=request.form,
            ), 400

        recipe.name = recipe_data['name']
        recipe.description = recipe_data['description']
        recipe.ingredients = recipe_data['ingredients']
        recipe.instructions = recipe_data['instructions']
        recipe.photo = recipe_data['photo']
        recipe.category_id = recipe_data['category_id']

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("The recipe could not be updated. Please try again.", 'error')
            return render_template(
                'edit_recipe.html',
                recipe=recipe,
                categories=categories,
                form_data=request.form,
            ), 409

        flash("Recipe updated successfully.", 'success')
        return redirect(url_for('recipe_bp.dashboard'))

    return render_template(
        'edit_recipe.html',
        recipe=recipe,
        categories=categories,
        form_data={},
    )


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
