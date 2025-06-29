import pymysql
from datetime import datetime

# DB credentials
db_host = "92.205.7.84"
db_port = 3306
db_user = "janabboud"
db_pass = "99uoZ2CejfzC"
db_name = "foodworld"

# Connect to DB
conn = pymysql.connect(host=db_host,
                       port=db_port,
                       user=db_user,
                       password=db_pass,
                       database=db_name,
                       charset="utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)

print("✅ Connected to DB.")

recipes = [

    # ---------------------
    # BREAKFAST
    # ---------------------
    {
        "name": "Banana Pancakes",
        "description": "Soft pancakes flavored with ripe bananas.",
        "ingredients": "bananas, flour, eggs, baking powder, milk, butter",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Banana_pancakes.jpg/320px-Banana_pancakes.jpg",
        "instructions":
        "Mash bananas, mix batter, cook on griddle until golden."
    },
    {
        "name": "Greek Yogurt Parfait",
        "description": "Layered yogurt with fruit and granola.",
        "ingredients": "Greek yogurt, berries, granola, honey",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Yogurt_parfait.jpg/320px-Yogurt_parfait.jpg",
        "instructions": "Layer yogurt, fruit, and granola in a glass."
    },
    {
        "name": "Bagel with Cream Cheese",
        "description": "Toasted bagel with creamy spread.",
        "ingredients": "bagels, cream cheese",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Bagel_with_cream_cheese.jpg/320px-Bagel_with_cream_cheese.jpg",
        "instructions": "Toast bagel, spread with cream cheese."
    },
    {
        "name": "Muesli Bowl",
        "description": "Cold cereal with oats, nuts, and fruit.",
        "ingredients": "rolled oats, nuts, raisins, milk",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Muesli_bowl.jpg/320px-Muesli_bowl.jpg",
        "instructions": "Combine oats, nuts, and milk, let soak overnight."
    },
    {
        "name": "Chia Seed Pudding",
        "description": "Creamy pudding made with chia seeds.",
        "ingredients": "chia seeds, almond milk, vanilla, maple syrup",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Chia_seed_pudding.jpg/320px-Chia_seed_pudding.jpg",
        "instructions": "Mix ingredients, chill overnight until thick."
    },
    {
        "name": "Breakfast Quesadilla",
        "description": "Tortilla filled with eggs and cheese.",
        "ingredients": "tortillas, eggs, cheese, spinach",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fb/Breakfast_quesadilla.jpg/320px-Breakfast_quesadilla.jpg",
        "instructions": "Scramble eggs, fill tortilla, grill until golden."
    },
    {
        "name": "Berry Smoothie",
        "description": "Refreshing drink made from blended berries.",
        "ingredients": "mixed berries, yogurt, honey",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Berry_smoothie.jpg/320px-Berry_smoothie.jpg",
        "instructions": "Blend all ingredients until smooth."
    },
    {
        "name": "Cinnamon Roll",
        "description": "Soft roll with cinnamon filling and icing.",
        "ingredients": "flour, sugar, cinnamon, butter, yeast",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Cinnamon_Rolls.jpg/320px-Cinnamon_Rolls.jpg",
        "instructions": "Prepare dough, roll with filling, bake and ice."
    },
    {
        "name": "English Muffin Sandwich",
        "description": "Egg, cheese, and ham on an English muffin.",
        "ingredients": "English muffins, eggs, cheese, ham",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Egg_McMuffin.jpg/320px-Egg_McMuffin.jpg",
        "instructions": "Cook egg, assemble sandwich with cheese and ham."
    },
    {
        "name": "Granola Bars",
        "description": "Chewy bars with oats and nuts.",
        "ingredients": "oats, honey, nuts, dried fruit",
        "category": "Breakfast",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Granola_bars.jpg/320px-Granola_bars.jpg",
        "instructions":
        "Mix ingredients, press into pan, chill, slice into bars."
    },

    # ---------------------
    # LUNCH
    # ---------------------
    {
        "name": "BLT Sandwich",
        "description": "Bacon, lettuce, and tomato sandwich.",
        "ingredients": "bacon, lettuce, tomato, bread, mayonnaise",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/BLT_sandwich.jpg/320px-BLT_sandwich.jpg",
        "instructions": "Layer ingredients on toasted bread."
    },
    {
        "name": "Chicken Shawarma Wrap",
        "description": "Middle Eastern wrap with spiced chicken.",
        "ingredients": "chicken, pita, garlic sauce, lettuce, tomato",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Chicken_shawarma_wrap.jpg/320px-Chicken_shawarma_wrap.jpg",
        "instructions": "Cook chicken with spices, wrap in pita with veggies."
    },
    {
        "name": "Tuna Salad Sandwich",
        "description": "Classic tuna salad between bread slices.",
        "ingredients": "tuna, mayonnaise, celery, bread",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Tuna_salad_sandwich.jpg/320px-Tuna_salad_sandwich.jpg",
        "instructions": "Mix tuna salad, spread on bread."
    },
    {
        "name": "Chicken Fajita Bowl",
        "description": "Mexican-style rice bowl with chicken and veggies.",
        "ingredients": "chicken, bell peppers, rice, salsa, avocado",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Chicken_fajita_bowl.jpg/320px-Chicken_fajita_bowl.jpg",
        "instructions": "Cook chicken and veggies, serve over rice."
    },
    {
        "name": "Pesto Pasta Salad",
        "description": "Cold pasta salad with pesto dressing.",
        "ingredients": "pasta, pesto, cherry tomatoes, mozzarella",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Pesto_pasta_salad.jpg/320px-Pesto_pasta_salad.jpg",
        "instructions": "Toss cooked pasta with pesto and veggies."
    },
    {
        "name": "Turkey Bacon Wrap",
        "description": "Wrap with turkey, bacon, and ranch.",
        "ingredients": "tortilla, turkey, bacon, lettuce, ranch dressing",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Turkey_wrap.jpg/320px-Turkey_wrap.jpg",
        "instructions": "Layer ingredients in tortilla, wrap and slice."
    },
    {
        "name": "Veggie Burrito",
        "description": "Burrito stuffed with beans and veggies.",
        "ingredients": "tortilla, rice, black beans, bell peppers, salsa",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Veggie_burrito.jpg/320px-Veggie_burrito.jpg",
        "instructions": "Fill tortilla with veggies and beans, wrap tightly."
    },
    {
        "name": "Egg Salad Sandwich",
        "description": "Chopped egg salad in a sandwich.",
        "ingredients": "eggs, mayonnaise, mustard, bread",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Egg_salad_sandwich.jpg/320px-Egg_salad_sandwich.jpg",
        "instructions": "Mix egg salad, spread on bread."
    },
    {
        "name": "Sushi Rolls",
        "description": "Rice rolls with vegetables and fish.",
        "ingredients": "rice, seaweed, cucumber, avocado, fish",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/Sushi_rolls.jpg/320px-Sushi_rolls.jpg",
        "instructions": "Roll rice and fillings in seaweed, slice into pieces."
    },
    {
        "name": "Asian Noodle Salad",
        "description": "Cold noodles with sesame dressing.",
        "ingredients": "noodles, carrots, bell peppers, sesame oil, soy sauce",
        "category": "Lunch",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Asian_noodle_salad.jpg/320px-Asian_noodle_salad.jpg",
        "instructions": "Toss noodles with veggies and sauce."
    },

    # ---------------------
    # DINNER
    # ---------------------
    {
        "name": "Beef Stroganoff",
        "description": "Tender beef in creamy mushroom sauce over noodles.",
        "ingredients": "beef, mushrooms, onion, sour cream, noodles",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Beef_Stroganoff.jpg/320px-Beef_Stroganoff.jpg",
        "instructions": "Cook beef and mushrooms, stir in cream sauce."
    },
    {
        "name": "Shrimp Scampi",
        "description": "Shrimp sautéed with garlic and butter.",
        "ingredients": "shrimp, garlic, butter, lemon, pasta",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Shrimp_Scampi.jpg/320px-Shrimp_Scampi.jpg",
        "instructions": "Cook shrimp in garlic butter, toss with pasta."
    },
    {
        "name": "Roast Chicken",
        "description": "Classic oven-roasted chicken.",
        "ingredients": "chicken, olive oil, garlic, rosemary",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Roast_chicken.jpg/320px-Roast_chicken.jpg",
        "instructions": "Season chicken, roast until golden brown."
    },
    {
        "name": "Pork Chops",
        "description": "Pan-seared pork chops with herbs.",
        "ingredients": "pork chops, olive oil, thyme, garlic",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Pork_chops.jpg/320px-Pork_chops.jpg",
        "instructions": "Sear pork chops, cook through with herbs."
    },
    {
        "name": "Vegetable Curry",
        "description": "Spicy curry with mixed vegetables.",
        "ingredients": "carrots, potatoes, peas, coconut milk, curry powder",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Vegetable_curry.jpg/320px-Vegetable_curry.jpg",
        "instructions": "Cook veggies in curry sauce until tender."
    },
    {
        "name": "Chicken Parmesan",
        "description": "Breaded chicken with marinara and cheese.",
        "ingredients":
        "chicken breasts, breadcrumbs, marinara sauce, mozzarella",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Chicken_Parmesan.jpg/320px-Chicken_Parmesan.jpg",
        "instructions": "Bread chicken, fry, top with sauce and cheese, bake."
    },
    {
        "name": "Lasagna",
        "description": "Layered pasta dish with meat and cheese.",
        "ingredients":
        "lasagna noodles, ricotta, beef, marinara sauce, mozzarella",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Lasagna_bolognese.jpg/320px-Lasagna_bolognese.jpg",
        "instructions": "Layer noodles with meat sauce and cheese, bake."
    },
    {
        "name": "Ratatouille",
        "description": "French dish of stewed vegetables.",
        "ingredients": "eggplant, zucchini, bell peppers, tomatoes, garlic",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Ratatouille.jpg/320px-Ratatouille.jpg",
        "instructions": "Layer sliced vegetables, bake until tender."
    },
    {
        "name": "Steak Frites",
        "description": "Grilled steak with French fries.",
        "ingredients": "steak, potatoes, butter, garlic",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Steak_frites.jpg/320px-Steak_frites.jpg",
        "instructions": "Grill steak, serve with crispy fries."
    },
    {
        "name": "Chili Con Carne",
        "description": "Spicy stew with beef and beans.",
        "ingredients": "ground beef, kidney beans, tomatoes, chili powder",
        "category": "Dinner",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Chili_con_carne.jpg/320px-Chili_con_carne.jpg",
        "instructions": "Simmer all ingredients until thick."
    },

    # ---------------------
    # SNACKS
    # ---------------------
    {
        "name": "Hummus",
        "description": "Chickpea dip with tahini.",
        "ingredients": "chickpeas, tahini, lemon juice, garlic",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Hummus.jpg/320px-Hummus.jpg",
        "instructions": "Blend all ingredients until smooth."
    },
    {
        "name": "Nachos",
        "description": "Tortilla chips loaded with toppings.",
        "ingredients": "tortilla chips, cheese, jalapenos, salsa",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Nachos.jpg/320px-Nachos.jpg",
        "instructions":
        "Layer chips, cheese, bake until melted, top with salsa."
    },
    {
        "name": "Cheese Platter",
        "description": "Selection of cheeses with crackers.",
        "ingredients": "assorted cheeses, crackers, grapes",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Cheese_platter.jpg/320px-Cheese_platter.jpg",
        "instructions": "Arrange cheeses and accompaniments on platter."
    },
    {
        "name": "Peanut Butter Celery Sticks",
        "description": "Crunchy celery filled with peanut butter.",
        "ingredients": "celery, peanut butter, raisins",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Celery_peanut_butter.jpg/320px-Celery_peanut_butter.jpg",
        "instructions":
        "Fill celery sticks with peanut butter, top with raisins."
    },
    {
        "name": "Mozzarella Sticks",
        "description": "Breaded fried cheese sticks.",
        "ingredients": "mozzarella cheese, breadcrumbs, eggs, oil",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Mozzarella_sticks.jpg/320px-Mozzarella_sticks.jpg",
        "instructions": "Bread cheese sticks, fry until golden."
    },
    {
        "name": "Mixed Nuts",
        "description": "Assorted salted nuts.",
        "ingredients": "cashews, almonds, peanuts, pecans",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Mixed_nuts.jpg/320px-Mixed_nuts.jpg",
        "instructions": "Mix nuts in bowl."
    },
    {
        "name": "Fruit Cups",
        "description": "Mixed fresh fruit in a cup.",
        "ingredients": "melon, pineapple, grapes, berries",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Fruit_cup.jpg/320px-Fruit_cup.jpg",
        "instructions": "Chop fruit, mix and serve chilled."
    },
    {
        "name": "Edamame",
        "description": "Steamed soybeans with salt.",
        "ingredients": "edamame, sea salt",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Edamame.jpg/320px-Edamame.jpg",
        "instructions": "Steam edamame, sprinkle with salt."
    },
    {
        "name": "Rice Cakes",
        "description": "Crispy puffed rice snacks.",
        "ingredients": "rice cakes, peanut butter, banana slices",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Rice_cakes_with_banana.jpg/320px-Rice_cakes_with_banana.jpg",
        "instructions": "Spread peanut butter on rice cakes, top with banana."
    },
    {
        "name": "Chocolate Dipped Strawberries",
        "description": "Fresh strawberries dipped in chocolate.",
        "ingredients": "strawberries, dark chocolate",
        "category": "Snacks",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Chocolate_dipped_strawberries.jpg/320px-Chocolate_dipped_strawberries.jpg",
        "instructions": "Dip strawberries in melted chocolate, chill to set."
    },

    # ---------------------
    # APPETIZERS
    # ---------------------
    {
        "name":
        "Caprese Skewers",
        "description":
        "Tomato, basil, and mozzarella on skewers.",
        "ingredients":
        "cherry tomatoes, basil, mozzarella balls, balsamic glaze",
        "category":
        "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Caprese_skewers.jpg/320px-Caprese_skewers.jpg",
        "instructions":
        "Thread tomatoes, basil, and cheese on skewers, drizzle with glaze."
    },
    {
        "name": "Spinach Artichoke Dip",
        "description": "Creamy dip with spinach and artichokes.",
        "ingredients": "spinach, artichoke hearts, cream cheese, parmesan",
        "category": "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/Spinach_artichoke_dip.jpg/320px-Spinach_artichoke_dip.jpg",
        "instructions": "Mix ingredients, bake until bubbly."
    },
    {
        "name": "Baked Brie",
        "description": "Warm, melty brie cheese wrapped in pastry.",
        "ingredients": "brie, puff pastry, honey, nuts",
        "category": "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Baked_brie.jpg/320px-Baked_brie.jpg",
        "instructions": "Wrap brie in pastry, bake until golden."
    },
    {
        "name": "Crostini",
        "description": "Small toasted bread slices with toppings.",
        "ingredients": "baguette, tomatoes, garlic, olive oil",
        "category": "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Crostini.jpg/320px-Crostini.jpg",
        "instructions": "Toast bread, top with tomato mixture."
    },
    {
        "name": "Buffalo Wings",
        "description": "Spicy chicken wings.",
        "ingredients": "chicken wings, hot sauce, butter",
        "category": "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Buffalo_wings.jpg/320px-Buffalo_wings.jpg",
        "instructions": "Fry wings, toss in sauce."
    },
    {
        "name": "Ceviche",
        "description": "Seafood marinated in citrus juice.",
        "ingredients": "shrimp, lime juice, tomato, onion, cilantro",
        "category": "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Ceviche.jpg/320px-Ceviche.jpg",
        "instructions": "Marinate seafood in citrus juice until opaque."
    },
    {
        "name": "Samosas",
        "description": "Fried pastries filled with spiced potatoes.",
        "ingredients": "potatoes, peas, flour, spices",
        "category": "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Samosas.jpg/320px-Samosas.jpg",
        "instructions": "Fill pastry with potatoes, fold, fry until crisp."
    },
    {
        "name": "Antipasto Platter",
        "description": "Italian platter of meats, cheeses, and olives.",
        "ingredients": "salami, prosciutto, cheese, olives",
        "category": "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Antipasto_platter.jpg/320px-Antipasto_platter.jpg",
        "instructions": "Arrange meats and cheeses on platter."
    },
    {
        "name": "Garlic Knots",
        "description": "Bread knots brushed with garlic butter.",
        "ingredients": "pizza dough, garlic, butter, parsley",
        "category": "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Garlic_knots.jpg/320px-Garlic_knots.jpg",
        "instructions": "Tie dough into knots, bake, brush with butter."
    },
    {
        "name": "Pigs in a Blanket",
        "description": "Mini sausages wrapped in pastry.",
        "ingredients": "mini sausages, puff pastry, egg wash",
        "category": "Appetizers",
        "photo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Pigs_in_a_blanket.jpg/320px-Pigs_in_a_blanket.jpg",
        "instructions": "Wrap sausages in pastry, bake until golden."
    }
]

success = 0
fail = 0

try:
    with conn.cursor() as cursor:
        for r in recipes:
            # Find category_id from category name
            cursor.execute("SELECT id FROM categories WHERE name = %s",
                           (r["category"], ))
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
            params = (r["name"], r["description"], r["ingredients"],
                      datetime.utcnow(), datetime.utcnow(), r["photo"],
                      r["instructions"], category_id)

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
