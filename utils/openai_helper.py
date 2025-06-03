import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # We'll define this in a moment

def generate_recipe_recommendation(ingredients, num_people):
    prompt = (
        f"You are a recipe suggestion AI. I have these ingredients: {', '.join(ingredients)}.\n"
        f"I am cooking for {num_people} people.\n"
        "Suggest 3 recipe ideas that I can make with those ingredients. "
        "Each idea should include a name and a short description.\n"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )

        ideas = response['choices'][0]['message']['content']
        return ideas.strip()

    except Exception as e:
        return f"Error generating recipe ideas: {e}"

