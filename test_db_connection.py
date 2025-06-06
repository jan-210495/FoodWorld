import pymysql

# Replace with your database credentials
host = "92.205.7.84"
port = 3306
user = "janabboud"
password = "99uoZ2CejfzC"
database = "foodworld"

try:
    connection = pymysql.connect(host=host,
                                 port=port,
                                 user=user,
                                 password=password,
                                 database=database)
    print("✅ Successfully connected to the database!")
    connection.close()
except pymysql.MySQLError as e:
    print("❌ Failed to connect to the database.")
    print(f"Error: {e}")
