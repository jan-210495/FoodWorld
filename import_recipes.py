import pymysql
from datetime import datetime

# ✅ Correct Railway DB credentials from your remote variables:
db_host = "92.205.7.84"
db_port = 3306
db_user = "janabboud"
db_pass = "99uoZ2CejfzC"
db_name = "foodworld"

# Connect to MySQL
conn = pymysql.connect(host=db_host,
                       port=db_port,
                       user=db_user,
                       password=db_pass,
                       database=db_name,
                       charset="utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)

print("✅ Connected to DB.")

# --- Recipes to insert (add more as needed) ---
recipes = [
    # ================================
    # BREAKFAST
    # ================================
    {
        "name":
        "Classic Pancakes",
        "description":
        "Fluffy golden pancakes for a perfect morning.",
        "ingredients":
        "2 cups flour, 2 eggs, 1.5 cups milk, 2 tbsp sugar, 1 tsp baking powder, pinch salt",
        "instructions":
        "Whisk dry ingredients. Add eggs and milk. Cook on hot griddle until bubbles form. Flip and cook another minute. Serve with syrup.",
        "category":
        "Breakfast",
        "photo":
        "https://images.unsplash.com/photo-1554109489-8b52d7f3f3a1?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Avocado Toast",
        "description":
        "Creamy avocado spread over toasted bread.",
        "ingredients":
        "2 slices bread, 1 ripe avocado, salt, pepper, lemon juice, chili flakes",
        "instructions":
        "Toast bread. Smash avocado with salt, pepper, lemon juice. Spread on toast. Sprinkle chili flakes.",
        "category":
        "Breakfast",
        "photo":
        "https://images.unsplash.com/photo-1559622214-60d9db7f37d3?fit=crop&w=800&q=80"
    },
    {
        "name":
        "French Omelette",
        "description":
        "Soft, delicate French omelette.",
        "ingredients":
        "3 eggs, 1 tbsp butter, pinch salt, chopped chives",
        "instructions":
        "Whisk eggs. Melt butter in pan. Pour eggs and stir gently until just set. Fold and slide onto plate.",
        "category":
        "Breakfast",
        "photo":
        "https://images.unsplash.com/photo-1618918446519-cdf33e39fb8f?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Smoothie Bowl",
        "description":
        "A vibrant smoothie bowl with fruit toppings.",
        "ingredients":
        "1 banana, 1 cup frozen berries, 1/2 cup yogurt, toppings: granola, coconut, fresh fruit",
        "instructions":
        "Blend banana, berries, yogurt. Pour into bowl. Top with granola, fruit, coconut.",
        "category":
        "Breakfast",
        "photo":
        "https://images.unsplash.com/photo-1502741338009-cac2772e18bc?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Breakfast Burrito",
        "description":
        "Tortilla wrapped with eggs, cheese, and veggies.",
        "ingredients":
        "Flour tortilla, scrambled eggs, cheddar cheese, bell peppers, onions",
        "instructions":
        "Sauté veggies. Scramble eggs. Fill tortilla with eggs, veggies, cheese. Roll up and grill lightly.",
        "category":
        "Breakfast",
        "photo":
        "https://images.unsplash.com/photo-1604908177522-b64638970551?fit=crop&w=800&q=80"
    },

    # ================================
    # LUNCH
    # ================================
    {
        "name":
        "Chicken Caesar Salad",
        "description":
        "Crisp lettuce with grilled chicken and Caesar dressing.",
        "ingredients":
        "Romaine lettuce, grilled chicken breast, Caesar dressing, croutons, parmesan cheese",
        "instructions":
        "Grill chicken. Toss lettuce with dressing. Top with chicken, croutons, parmesan.",
        "category":
        "Lunch",
        "photo":
        "https://images.unsplash.com/photo-1572449043412-55f4685c1df2?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Caprese Sandwich",
        "description":
        "Fresh mozzarella, tomatoes, and basil in ciabatta.",
        "ingredients":
        "Ciabatta bread, fresh mozzarella, tomatoes, basil, olive oil, balsamic glaze",
        "instructions":
        "Slice bread. Layer cheese, tomatoes, basil. Drizzle with oil and glaze. Press sandwich lightly.",
        "category":
        "Lunch",
        "photo":
        "https://images.unsplash.com/photo-1629444605829-0d918527d106?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Quinoa Salad",
        "description":
        "Healthy quinoa with veggies and lemon dressing.",
        "ingredients":
        "Quinoa, cucumber, tomato, red onion, parsley, lemon juice, olive oil",
        "instructions":
        "Cook quinoa. Cool slightly. Mix with chopped veggies. Dress with lemon juice and oil.",
        "category":
        "Lunch",
        "photo":
        "https://images.unsplash.com/photo-1605514926630-07a5b910dce9?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Turkey Wrap",
        "description":
        "Whole wheat wrap with turkey, lettuce, and cheese.",
        "ingredients":
        "Whole wheat tortilla, turkey slices, lettuce, cheddar, mayo",
        "instructions":
        "Layer turkey, lettuce, cheese. Spread mayo. Roll and slice.",
        "category":
        "Lunch",
        "photo":
        "https://images.unsplash.com/photo-1605475128032-7a92ebbb6300?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Minestrone Soup",
        "description":
        "Classic Italian vegetable soup.",
        "ingredients":
        "Onion, carrot, celery, zucchini, tomato, pasta, vegetable broth, herbs",
        "instructions":
        "Sauté vegetables. Add broth and tomatoes. Simmer. Add pasta. Cook until pasta is tender.",
        "category":
        "Lunch",
        "photo":
        "https://images.unsplash.com/photo-1616177134563-7a31f062b671?fit=crop&w=800&q=80"
    },

    # ================================
    # DINNER
    # ================================
    {
        "name":
        "Spaghetti Bolognese",
        "description":
        "Classic pasta with savory meat sauce.",
        "ingredients":
        "Spaghetti, ground beef, onion, garlic, tomato sauce, Italian herbs",
        "instructions":
        "Cook spaghetti. Brown beef with onions and garlic. Add tomato sauce and herbs. Simmer. Serve over pasta.",
        "category":
        "Dinner",
        "photo":
        "https://images.unsplash.com/photo-1608133646684-46e30b944ae5?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Beef Stir Fry",
        "description":
        "Beef and colorful veggies in soy garlic sauce.",
        "ingredients":
        "Beef strips, broccoli, bell peppers, soy sauce, garlic, ginger",
        "instructions":
        "Stir fry beef. Add veggies. Pour in sauce. Cook until veggies are crisp-tender.",
        "category":
        "Dinner",
        "photo":
        "https://images.unsplash.com/photo-1601924570707-3ccdb868b478?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Salmon with Lemon Butter",
        "description":
        "Baked salmon with a lemon butter sauce.",
        "ingredients":
        "Salmon fillets, butter, lemon juice, garlic, parsley",
        "instructions":
        "Bake salmon. Melt butter with lemon and garlic. Pour over fish and garnish with parsley.",
        "category":
        "Dinner",
        "photo":
        "https://images.unsplash.com/photo-1613131149964-1ccdf8c2b00d?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Chicken Alfredo",
        "description":
        "Creamy pasta with chicken breast slices.",
        "ingredients":
        "Fettuccine pasta, chicken breast, heavy cream, parmesan, garlic, butter",
        "instructions":
        "Cook pasta. Sauté chicken. Add cream, garlic, and cheese. Toss with pasta.",
        "category":
        "Dinner",
        "photo":
        "https://images.unsplash.com/photo-1613131149964-1ccdf8c2b00d?fit=crop&w=800&q=80"
    },
    {
        "name":
        "Stuffed Peppers",
        "description":
        "Bell peppers stuffed with rice and ground beef.",
        "ingredients":
        "Bell peppers, ground beef, cooked rice, tomato sauce, onion, garlic, herbs",
        "instructions":
        "Sauté beef with onion and garlic. Mix with rice and sauce. Stuff peppers. Bake until tender.",
        "category":
        "Dinner",
        "photo":
        "https://images.unsplash.com/photo-1608571429648-5ba7f4a694ed?fit=crop&w=800&q=80"
    },
]

success = 0
fail = 0

try:
    with conn.cursor() as cursor:
        for recipe in recipes:
            try:
                sql = """
                    INSERT INTO recipes
                        (name, description, ingredients, category, photo, instructions, created_at, updated_at)
                    VALUES
                        (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                params = (recipe["name"], recipe["description"],
                          recipe["ingredients"], recipe["category"],
                          recipe["photo"], recipe["instructions"],
                          datetime.utcnow(), datetime.utcnow())
                cursor.execute(sql, params)
                success += 1
            except Exception as e:
                print("❌ Error inserting recipe:", recipe["name"], "→", e)
                fail += 1

    conn.commit()
    print(f"✅ Done! Inserted {success} recipes. Failures: {fail}")

finally:
    conn.close()
