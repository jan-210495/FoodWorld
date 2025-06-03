from utils.openai_helper import generate_recipe_recommendation

@recipe_bp.route('/recommend', methods=['POST'])
def recommend_recipe():
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    num_people = data.get('num_people', 1)

    if not ingredients or not isinstance(ingredients, list):
        return jsonify({"error": "Ingredients must be a list"}), 400

    suggestions = generate_recipe_recommendation(ingredients, num_people)
    return jsonify({"suggestions": suggestions})

