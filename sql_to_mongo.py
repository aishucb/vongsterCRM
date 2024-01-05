import mysql.connector
from pymongo import MongoClient

# MySQL Database credentials
mysql_db_config = {
    'host': '127.0.0.1',
    'user': 'vongle',
    'password': 'ashiv3377',
    'database': 'osqacademy',
}

# MongoDB credentials
mongo_uri = "mongodb+srv://vongledata:1UVw7DhRKcRQJPY3@cluster0.t3ujmhu.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client.get_database("Vongdata")
mongo_collection = mongo_db.get_collection("test3")  # Update with the actual collection name

# File to store results
output_file = "result.txt"

try:
    # Establish a connection to the MySQL server
    mysql_connection = mysql.connector.connect(**mysql_db_config)

    if mysql_connection.is_connected():
        print("Connected to MySQL database")

        # Create a cursor object to execute SQL queries
        cursor = mysql_connection.cursor()

        # Execute a SELECT query to get the list of usernames from MySQL
        query = "SELECT id, username,department,firstname,lastname,email,phone1,address,city,institution,idnumber,firstnamephonetic FROM mdl_user"
        cursor.execute(query)

        # Fetch all the rows
        usernames = cursor.fetchall()

        # Open the file in append mode
        with open(output_file, "a") as result_file:
            # Check each username in MongoDB
            # ...

            for username_tuple in usernames:
                user_id, username, department, firstname, lastname, email, phone1, address, city, institution,grade,house = username_tuple
                if department != 'vongster':
                    continue


                mongo_query = {"full_name": username}
                result = mongo_collection.find_one(mongo_query)

                if result:
                    print(f"Document found in MongoDB for username {username}")
                    result_file.write(f"Document found for username {username}\n")
                else:
                    print(f"No document found in MongoDB for username {username}")
                    result_file.write(f"No document found for username {username}\n")


                collection = mongo_db['test3']  # Use the Database object
                data_to_insert = {
                    'roll_number': user_id,
                    'full_name': username,
                    'firstname': firstname,
                    'lastname': lastname,
                    'email': email,
                'phone': phone1,
                'address': address,
                'city': city,
                'institution': institution,
                'active': 'active',
                'grade': grade,
                'house' : house
                }
                activity = f"user_{user_id}"
        # Check if the collection already exists
                if activity not in mongo_db.list_collection_names():
                    collection.insert_one(data_to_insert)
                    mongo_db.create_collection(activity)

except mysql.connector.Error as e:
    print(f"Error: {e}")

finally:
    # Close the cursor and connection for MySQL
    if 'cursor' in locals():
        cursor.close()
    if 'mysql_connection' in locals() and mysql_connection.is_connected():
        mysql_connection.close()
        print("MySQL Connection closed")

    # Close the connection for MongoDB
    if 'mongo_client' in locals():
        mongo_client.close()
        print("MongoDB Connection closed")