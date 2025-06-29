import pymysql
from datetime import datetime

# DB credentials
db_host = "92.205.7.84"
db_port = 3306
db_user = "janabboud"
db_pass = "99uoZ2CejfzC"
db_name = "foodworld"

# Connect to DB
conn = pymysql.connect(
    host=db_host,
    port=db_port,
    user=db_user,
    password=db_pass,
    database=db_name,
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

print("✅ Connected to DB.")

recipes = [

    # ➤ Category: Pizza
    {
        "name": "Margherita Pizza",
        "description": "Classic Italian pizza with tomato, mozzarella, and basil.",
        "ingredients": "pizza dough, tomato sauce, mozzarella cheese, basil, olive oil",
        "category": "Pizza",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Supreme_pizza.jpg/320px-Supreme_pizza.jpg",
        "instructions": "Spread sauce on dough, add cheese and basil. Bake at 250°C until golden."
    },
    {
        "name": "Pepperoni Pizza",
        "description": "Popular pizza topped with spicy pepperoni slices and mozzarella.",
        "ingredients": "pizza dough, tomato sauce, mozzarella, pepperoni",
        "category": "Pizza",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Eq_it-na_pizza-margherita_sep2005_sml.jpg/320px-Eq_it-na_pizza-margherita_sep2005_sml.jpg",
        "instructions": "Top sauce and cheese with pepperoni. Bake at 220°C for 15 minutes."
    },
    {
        "name": "BBQ Chicken Pizza",
        "description": "Smoky BBQ sauce with chicken and onions on pizza crust.",
        "ingredients": "pizza dough, BBQ sauce, chicken, red onion, mozzarella",
        "category": "Pizza",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/BBQ_chicken_pizza.jpg/320px-BBQ_chicken_pizza.jpg",
        "instructions": "Spread BBQ sauce, top with chicken, onions, and cheese. Bake until golden."
    },
    {
        "name": "Hawaiian Pizza",
        "description": "Pizza topped with ham and pineapple.",
        "ingredients": "pizza dough, tomato sauce, ham, pineapple, mozzarella",
        "category": "Pizza",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Hawaiian_pizza.jpg/320px-Hawaiian_pizza.jpg",
        "instructions": "Add sauce, cheese, ham, and pineapple. Bake at 230°C for 12 minutes."
    },
    {
        "name": "Four Cheese Pizza",
        "description": "Creamy pizza with a blend of four cheeses.",
        "ingredients": "pizza dough, mozzarella, gorgonzola, parmesan, provolone, tomato sauce",
        "category": "Pizza",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Four_cheese_pizza.jpg/320px-Four_cheese_pizza.jpg",
        "instructions": "Top dough with sauce and all cheeses. Bake at 220°C for 10-12 minutes."
    },

    # ➤ Category: Salads
    {
        "name": "Caesar Salad",
        "description": "Crisp romaine lettuce with creamy Caesar dressing.",
        "ingredients": "romaine lettuce, Caesar dressing, croutons, parmesan",
        "category": "Salads",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Caesar_salad_%281%29.jpg/320px-Caesar_salad_%281%29.jpg",
        "instructions": "Toss lettuce with dressing, top with croutons and cheese."
    },
    {
        "name": "Greek Salad",
        "description": "Fresh salad with tomato, cucumber, olives, and feta.",
        "ingredients": "tomatoes, cucumber, red onion, olives, feta, olive oil",
        "category": "Salads",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Greek_salad.jpg/320px-Greek_salad.jpg",
        "instructions": "Combine vegetables, drizzle olive oil, and sprinkle feta."
    },
    {
        "name": "Caprese Salad",
        "description": "Italian salad of tomato, mozzarella, and basil.",
        "ingredients": "tomatoes, mozzarella, fresh basil, olive oil, balsamic glaze",
        "category": "Salads",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Caprese_Salad.jpg/320px-Caprese_Salad.jpg",
        "instructions": "Layer tomato and mozzarella slices, drizzle with oil and balsamic."
    },
    {
        "name": "Quinoa Salad",
        "description": "Healthy salad with quinoa and vegetables.",
        "ingredients": "quinoa, bell peppers, cucumber, parsley, olive oil, lemon juice",
        "category": "Salads",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Quinoa_salad.jpg/320px-Quinoa_salad.jpg",
        "instructions": "Mix cooked quinoa with veggies and dressing."
    },
    {
        "name": "Coleslaw",
        "description": "Classic cabbage salad with creamy dressing.",
        "ingredients": "cabbage, carrot, mayonnaise, vinegar, sugar",
        "category": "Salads",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Coleslaw.jpg/320px-Coleslaw.jpg",
        "instructions": "Toss shredded cabbage and carrots with dressing."
    },

    # ➤ Category: Indian
    {
        "name": "Chicken Tikka Masala",
        "description": "Chicken in spiced tomato sauce.",
        "ingredients": "chicken, tomato puree, cream, spices",
        "category": "Indian",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Chicken_tikka_masala.jpg/320px-Chicken_tikka_masala.jpg",
        "instructions": "Cook chicken, add sauce and spices, simmer until thick."
    },
    {
        "name": "Palak Paneer",
        "description": "Cubes of paneer in creamy spinach sauce.",
        "ingredients": "paneer, spinach, onion, garlic, spices, cream",
        "category": "Indian",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Palak_Paneer.jpg/320px-Palak_Paneer.jpg",
        "instructions": "Puree spinach, cook with spices, add paneer cubes."
    },
    {
        "name": "Butter Chicken",
        "description": "Tender chicken in buttery tomato sauce.",
        "ingredients": "chicken, butter, tomato sauce, cream, spices",
        "category": "Indian",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Butter_chicken.jpg/320px-Butter_chicken.jpg",
        "instructions": "Cook chicken, add tomato sauce, butter, and cream."
    },
    {
        "name": "Aloo Gobi",
        "description": "Spiced potatoes and cauliflower.",
        "ingredients": "potatoes, cauliflower, onion, spices",
        "category": "Indian",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fc/Aloo_gobi.jpg/320px-Aloo_gobi.jpg",
        "instructions": "Sauté vegetables with spices until tender."
    },
    {
        "name": "Dal Tadka",
        "description": "Lentils cooked with onions, tomatoes, and spices.",
        "ingredients": "lentils, onion, tomato, garlic, spices, ghee",
        "category": "Indian",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Dal_Tadka.jpg/320px-Dal_Tadka.jpg",
        "instructions": "Cook lentils, add tempering of spices and ghee."
    },

    # ➤ Category: Soups
    {
        "name": "Tomato Soup",
        "description": "Creamy soup made from fresh tomatoes.",
        "ingredients": "tomatoes, onion, garlic, cream, vegetable broth",
        "category": "Soups",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Tomato_soup.jpg/320px-Tomato_soup.jpg",
        "instructions": "Cook tomatoes and onions, blend, and add cream."
    },
    {
        "name": "Minestrone Soup",
        "description": "Hearty Italian vegetable soup.",
        "ingredients": "beans, carrots, celery, pasta, tomatoes, broth",
        "category": "Soups",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/Minestrone.jpg/320px-Minestrone.jpg",
        "instructions": "Sauté veggies, add broth and pasta, cook until tender."
    },
    {
        "name": "Chicken Noodle Soup",
        "description": "Comforting soup with chicken and noodles.",
        "ingredients": "chicken, carrots, celery, noodles, broth",
        "category": "Soups",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Chicken_noodle_soup.jpg/320px-Chicken_noodle_soup.jpg",
        "instructions": "Simmer chicken, add veggies and noodles, cook until soft."
    },
    {
        "name": "French Onion Soup",
        "description": "Soup with caramelized onions and melted cheese.",
        "ingredients": "onions, beef broth, bread, gruyère cheese",
        "category": "Soups",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/French_Onion_Soup.jpg/320px-French_Onion_Soup.jpg",
        "instructions": "Caramelize onions, add broth, top with bread and cheese."
    },
    {
        "name": "Broccoli Cheddar Soup",
        "description": "Creamy soup with broccoli and cheddar.",
        "ingredients": "broccoli, cheddar, milk, butter, flour",
        "category": "Soups",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Broccoli_Cheddar_Soup.jpg/320px-Broccoli_Cheddar_Soup.jpg",
        "instructions": "Cook broccoli, blend with cheese sauce until smooth."
    }
]


success = 0
fail = 0

try:
    with conn.cursor() as cursor:
        for r in recipes:
            # Find category_id from category name
            cursor.execute("SELECT id FROM categories WHERE name = %s", (r["category"],))
            cat = cursor.fetchone()
            if not cat:
                print(f"❌ Category not found: {r['category']}")
                fail += 1
                continue

            category_id = cat["id"]

            sql = """
                INSERT INTO recipes
                (name, description, ingredients, created_at, updated_at, photo, instructions, category_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                r["name"],
                r["description"],
                r["ingredients"],
                datetime.utcnow(),
                datetime.utcnow(),
                r["photo"],
                r["instructions"],
                category_id
            )

            try:
                cursor.execute(sql, params)
                success += 1
            except Exception as e:
                print(f"❌ Error inserting {r['name']}: {e}")
                fail += 1

    conn.commit()
    print(f"✅ Done! Inserted {success} recipes. Failures: {fail}")

finally:
    conn.close()
