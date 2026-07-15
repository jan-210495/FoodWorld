"""Recipe, category, search, recommendation, and favorite routes."""


from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from extensions import limiter
from models import db
from models.category import Category
from models.favorite import Favorite
from models.recipe import Recipe
from utils.ai_helper import get_food_image, parse_recipe_response, query_gemini
from utils.auth import admin_required
from utils.validation import (
    clean_text,
    serialize_ingredients,
    validate_category_form,
    validate_recipe_form,
    validate_recommendation_input,
)

recipe_bp = Blueprint("recipe_bp", __name__, url_prefix="/recipes")


@recipe_bp.route("/recommend", methods=["POST"])
@limiter.limit("10 per hour")
def recommend():
    data, errors = validate_recommendation_input(request.form)
    if errors:
        for error in errors:
            flash(error, "error")
        return render_template(
            "search_results.html",
            ai_recipes=[],
            recommendation_input=request.form,
        ), 400

    servings = data["servings"] or 2
    prompt = f"""
Return exactly one JSON object and no markdown fences.
The object must have a `recipes` array containing up to 3 recipes.
Each recipe must contain:
- `title`: a short string
- `ingredients`: an array of ingredient strings
- `steps`: an array of instruction strings

Use these user-provided ingredients: {data['ingredients']}
The recipes should serve {servings} people.
Do not include HTML, image URLs, medical claims, or fields other than title, ingredients, and steps.
"""

    ai_response = query_gemini(prompt)
    ai_recipes = parse_recipe_response(ai_response)
    for recipe in ai_recipes:
        recipe["photo"] = get_food_image(recipe["title"])

    if not ai_recipes:
        flash("No recipe suggestions are available right now. Please try again later.", "error")

    return render_template(
        "search_results.html",
        ai_recipes=ai_recipes,
        recommendation_input=request.form,
    )


@recipe_bp.route("/recommend/substitute", methods=["POST"])
@limiter.limit("20 per hour")
def recommend_substitute():
    data = request.get_json(silent=True) or {}
    missing_ingredient = clean_text(data.get("missing_ingredient"))[:200]
    recipe_name = clean_text(data.get("recipe_name"))[:120]

    if not missing_ingredient:
        return jsonify({"suggestion": "Tell us which ingredient is missing."}), 400

    context = f" They are cooking {recipe_name}." if recipe_name else ""
    prompt = (
        f"A user is missing the ingredient {missing_ingredient}.{context} "
        "Suggest one or two practical substitutes in one short, plain-text answer."
    )
    suggestion = query_gemini(prompt) or "Sorry, I couldn't find a substitute this time."
    return jsonify({"suggestion": suggestion.strip()[:1_000]})


@recipe_bp.route("/", methods=["GET"])
def cards_page():
    category_id = request.args.get("category_id", type=int)
    category = db.get_or_404(Category, category_id) if category_id else None
    query = Recipe.query.options(selectinload(Recipe.category)).order_by(Recipe.name.asc())
    if category:
        query = query.filter_by(category_id=category.id)
    pagination = query.paginate(
        page=max(request.args.get("page", 1, type=int), 1),
        per_page=12,
        error_out=False,
    )
    return render_template(
        "cards.html",
        recipes=pagination.items,
        pagination=pagination,
        category=category,
    )


@recipe_bp.route("/<int:recipe_id>")
def recipe_detail(recipe_id):
    recipe = db.get_or_404(Recipe, recipe_id)
    favorite = None
    if current_user.is_authenticated:
        favorite = Favorite.query.filter_by(
            user_id=current_user.id,
            recipe_id=recipe.id,
        ).first()
    return render_template("recipe.html", recipe=recipe, favorite=favorite)


@recipe_bp.route("/<int:recipe_id>/favorite", methods=["POST"])
@login_required
def toggle_favorite(recipe_id):
    recipe = db.get_or_404(Recipe, recipe_id)
    favorite = Favorite.query.filter_by(
        user_id=current_user.id,
        recipe_id=recipe.id,
    ).first()
    if favorite:
        db.session.delete(favorite)
        message = "Recipe removed from saved recipes."
    else:
        db.session.add(Favorite(user_id=current_user.id, recipe_id=recipe.id))
        message = "Recipe saved to your dashboard."

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("The recipe could not be saved. Please try again.", "error")
    else:
        flash(message, "success")
    return redirect(url_for("recipe_bp.recipe_detail", recipe_id=recipe.id))


@recipe_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():
    pagination = Recipe.query.options(selectinload(Recipe.category)).order_by(
        Recipe.created_at.desc()
    ).paginate(
        page=max(request.args.get("page", 1, type=int), 1),
        per_page=25,
        error_out=False,
    )
    return render_template("dashboard.html", recipes=pagination.items, pagination=pagination)


@recipe_bp.route("/add", methods=["GET", "POST"])
@admin_required
def add_recipe():
    categories = Category.query.order_by(Category.name.asc()).all()

    if request.method == "POST":
        recipe_data, errors = validate_recipe_form(request.form)
        if not errors and db.session.get(Category, recipe_data["category_id"]) is None:
            errors.append("The selected category does not exist.")
        if not errors and Recipe.query.filter(Recipe.name == recipe_data["name"]).first():
            errors.append("A recipe with this name already exists.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "add_recipe.html",
                categories=categories,
                form_data=request.form,
            ), 400

        recipe = Recipe(
            name=recipe_data["name"],
            description=recipe_data["description"],
            ingredients=serialize_ingredients(recipe_data["ingredients"]),
            instructions=recipe_data["instructions"],
            photo=recipe_data["photo"],
            category_id=recipe_data["category_id"],
        )
        try:
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("The recipe could not be saved. Please try again.", "error")
            return render_template(
                "add_recipe.html",
                categories=categories,
                form_data=request.form,
            ), 409

        flash("Recipe added successfully.", "success")
        return redirect(url_for("recipe_bp.dashboard"))

    return render_template("add_recipe.html", categories=categories, form_data={})


@recipe_bp.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
@admin_required
def edit_recipe(recipe_id):
    recipe = db.get_or_404(Recipe, recipe_id)
    categories = Category.query.order_by(Category.name.asc()).all()

    if request.method == "POST":
        recipe_data, errors = validate_recipe_form(request.form)
        if not errors and db.session.get(Category, recipe_data["category_id"]) is None:
            errors.append("The selected category does not exist.")
        if not errors and Recipe.query.filter(
            Recipe.name == recipe_data["name"], Recipe.id != recipe.id
        ).first():
            errors.append("A recipe with this name already exists.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "edit_recipe.html",
                recipe=recipe,
                categories=categories,
                form_data=request.form,
            ), 400

        recipe.name = recipe_data["name"]
        recipe.description = recipe_data["description"]
        recipe.ingredients = serialize_ingredients(recipe_data["ingredients"])
        recipe.instructions = recipe_data["instructions"]
        recipe.photo = recipe_data["photo"]
        recipe.category_id = recipe_data["category_id"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("The recipe could not be updated. Please try again.", "error")
            return render_template(
                "edit_recipe.html",
                recipe=recipe,
                categories=categories,
                form_data=request.form,
            ), 409

        flash("Recipe updated successfully.", "success")
        return redirect(url_for("recipe_bp.dashboard"))

    return render_template(
        "edit_recipe.html",
        recipe=recipe,
        categories=categories,
        form_data={},
    )


@recipe_bp.route("/delete/<int:recipe_id>", methods=["POST"])
@admin_required
def delete_recipe(recipe_id):
    recipe = db.get_or_404(Recipe, recipe_id)
    try:
        db.session.delete(recipe)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("The recipe could not be deleted.", "error")
    else:
        flash("Recipe deleted successfully.", "success")
    return redirect(url_for("recipe_bp.dashboard"))


@recipe_bp.route("/categories")
def list_categories():
    categories = Category.query.options(selectinload(Category.recipes)).order_by(Category.name.asc()).all()
    return render_template("categories.html", categories=categories)


@recipe_bp.route("/category/<int:category_id>")
def recipes_by_category(category_id):
    category = db.get_or_404(Category, category_id)
    pagination = Recipe.query.options(selectinload(Recipe.category)).filter_by(
        category_id=category.id
    ).order_by(Recipe.name.asc()).paginate(
        page=max(request.args.get("page", 1, type=int), 1),
        per_page=12,
        error_out=False,
    )
    return render_template(
        "cards.html",
        recipes=pagination.items,
        pagination=pagination,
        category=category,
    )


@recipe_bp.route("/categories/add", methods=["GET", "POST"])
@admin_required
def add_category():
    if request.method == "POST":
        data, errors = validate_category_form(request.form)
        if not errors and Category.query.filter(Category.name == data["name"]).first():
            errors.append("A category with this name already exists.")
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("category_form.html", form_data=request.form), 400
        db.session.add(Category(name=data["name"], photo=data["photo"]))
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("The category could not be saved.", "error")
            return render_template("category_form.html", form_data=request.form), 409
        flash("Category added successfully.", "success")
        return redirect(url_for("recipe_bp.manage_categories"))
    return render_template("category_form.html", form_data={})


@recipe_bp.route("/categories/manage")
@admin_required
def manage_categories():
    categories = Category.query.options(selectinload(Category.recipes)).order_by(Category.name.asc()).all()
    return render_template("manage_categories.html", categories=categories)


@recipe_bp.route("/categories/edit/<int:category_id>", methods=["GET", "POST"])
@admin_required
def edit_category(category_id):
    category = db.get_or_404(Category, category_id)
    if request.method == "POST":
        data, errors = validate_category_form(request.form)
        duplicate = Category.query.filter(
            Category.name == data["name"], Category.id != category.id
        ).first()
        if not errors and duplicate:
            errors.append("A category with this name already exists.")
        if errors:
            for error in errors:
                flash(error, "error")
            return render_template(
                "category_form.html", form_data=request.form, category=category
            ), 400
        category.name = data["name"]
        category.photo = data["photo"]
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("The category could not be updated.", "error")
            return render_template(
                "category_form.html", form_data=request.form, category=category
            ), 409
        flash("Category updated successfully.", "success")
        return redirect(url_for("recipe_bp.manage_categories"))
    return render_template("category_form.html", form_data={}, category=category)


@recipe_bp.route("/categories/delete/<int:category_id>", methods=["POST"])
@admin_required
def delete_category(category_id):
    category = db.get_or_404(Category, category_id)
    if category.recipes:
        flash("Move or delete this category's recipes before deleting it.", "error")
        return redirect(url_for("recipe_bp.manage_categories"))
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted successfully.", "success")
    return redirect(url_for("recipe_bp.manage_categories"))


@recipe_bp.route("/search")
def search_recipes():
    query = clean_text(request.args.get("q"))[:100]
    recipes = []
    if query:
        pattern = f"%{query}%"
        recipes = Recipe.query.options(selectinload(Recipe.category)).filter(
            or_(
                Recipe.name.ilike(pattern),
                Recipe.description.ilike(pattern),
                Recipe.ingredients.ilike(pattern),
                Recipe.category.has(Category.name.ilike(pattern)),
            )
        ).order_by(Recipe.name.asc()).all()
    return render_template("search_results.html", recipes=recipes, query=query)
