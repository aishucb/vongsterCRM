import mysql.connector
from pymongo import MongoClient
from datetime import datetime
from decimal import Decimal  # Import Decimal type

# MySQL Database credentials
mysql_db_config = {
    'host': '127.0.0.1',
    'user': 'vongle',
    'password': 'ashiv3377',
    'database': 'osqacademy',
}

mongo_uri = "mongodb+srv://vongledata:1UVw7DhRKcRQJPY3@cluster0.t3ujmhu.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(mongo_uri)
mongo_db = mongo_client.get_database("Vongdata")

try:
    # Establish a connection to the MySQL server
    mysql_connection = mysql.connector.connect(**mysql_db_config)

    if mysql_connection.is_connected():
        print("Connected to MySQL database")

        cursor = mysql_connection.cursor()
        cursor2 = mysql_connection.cursor()
        query = "select id, userid, itemid, finalgrade, timecreated,timemodified from mdl_grade_grades;"
        query2 = "select id, itemname from mdl_grade_items;"
        cursor2.execute(query2)
        gradeitem = cursor2.fetchall()
        cursor.execute(query)
        usernames = cursor.fetchall()
        grade_items_dict = {}
        for grad_tuple in gradeitem:
            gradid, itemname = grad_tuple
            grade_items_dict[gradid] = itemname

        print(grade_items_dict)

        for username_tuple in usernames:
            id, user_id, itemid, finalgrade, timecreated,timemodified = username_tuple

            if timecreated is not None:
                mongo_collection = mongo_db.get_collection(str(user_id))
                mongo_query = {"id": id}
                result = mongo_collection.find_one(mongo_query)
                item_name = grade_items_dict.get(itemid, "Unknown Item")

                if result:
                    print(f"Document found in MongoDB")
                else:
                    if item_name is not None and finalgrade is not None:
                        unix_timestamp = timecreated
                        datetime_object = datetime.utcfromtimestamp(unix_timestamp)
                        month = datetime_object.month  # Adjust the format as needed

                        if isinstance(finalgrade, float):
                            finalgrade_value = finalgrade
                        elif isinstance(finalgrade, Decimal):
                            finalgrade_value = float(finalgrade)
                        else:
                            finalgrade_value = None

                        if finalgrade_value is not None:
                            data_to_insert = {
                                'id': id,
                                'mark': finalgrade_value,
                                'itemname': item_name,
                                'date': month
                            }
                            mongo_collection.insert_one(data_to_insert)
                        else:
                            print(f"Skipping record with id={id} because finalgrade is not a valid float value")
                    else:
                        print(f"Skipping record with id={id} because finalgrade is None")
            elif timemodified is not None :
                mongo_collection = mongo_db.get_collection(str(user_id))
                mongo_query = {"id": id}
                result = mongo_collection.find_one(mongo_query)
                item_name = grade_items_dict.get(itemid, "Unknown Item")

                if result:
                    print(f"Document found in MongoDB")
                else:
                    if item_name is not None and finalgrade is not None:
                        unix_timestamp = timecreated
                        datetime_object = datetime.utcfromtimestamp(unix_timestamp)
                        month = datetime_object.month  # Adjust the format as needed

                        if isinstance(finalgrade, float):
                            finalgrade_value = finalgrade
                        elif isinstance(finalgrade, Decimal):
                            finalgrade_value = float(finalgrade)
                        else:
                            finalgrade_value = None

                        if finalgrade_value is not None:
                            data_to_insert = {
                                'id': id,
                                'mark': finalgrade_value,
                                'itemname': item_name,
                                'date': month
                            }
                            mongo_collection.insert_one(data_to_insert)
                        else:
                            print(f"Skipping record with id={id} because finalgrade is not a valid float value")
                    else:
                        print(f"Skipping record with id={id} because finalgrade is None")
            else:    
                print(f"Skipping record with id={id} because timecreated is None")

except mysql.connector.Error as e:
    print(f"Error: {e}")
