import mysql.connector
import config

conn = mysql.connector.connect(host=config.DB_HOST,
                               user=config.DB_USER,
                               password=config.DB_PASSWORD,
                               database=config.DB_NAME)

cursor = conn.cursor()

# Get list of tables
cursor.execute("SHOW TABLES;")
tables = cursor.fetchall()

print("📋 Tables in your database:")
for (table_name, ) in tables:
    print(f"\n🔸 {table_name.upper()}")

    try:
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Print column headers
        print(" | ".join(columns))
        print("-" * (len(columns) * 20))

        if rows:
            for row in rows:
                print(" | ".join(str(cell) for cell in row))
        else:
            print(" (No rows found)")

    except Exception as e:
        print(f"⚠️ Error reading {table_name}: {e}")

cursor.close()
conn.close()
