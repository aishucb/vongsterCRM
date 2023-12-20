import mysql.connector
from pymongo import MongoClient

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
        query = "select id, userid, itemid, finalgrade from mdl_grade_grades;"
        query2 = "select id,itemname from  mdl_grade_items;"
        cursor2.execute(query2)
        gradeitem = cursor2.fetchall()
        cursor.execute(query)
        usernames = cursor.fetchall()
        grade_items_dict = {}
        for grad_tuple in gradeitem: 
            gradid,itemname=grad_tuple
            grade_items_dict[gradid]=itemname

        print(grade_items_dict) 

       
        for username_tuple in usernames:
            id, user_id, itemid,finalgrade = username_tuple
            mongo_collection = mongo_db.get_collection(str(user_id))
            mongo_query = {"id": id}
            result = mongo_collection.find_one(mongo_query)
            item_name = grade_items_dict.get(itemid)
            print(item_name)
            if result:
                print(f"Document found in MongoDB")
            else:
                if item_name is not None and finalgrade is not None:
                    if isinstance(finalgrade, float):
                        data_to_insert = {
                            'id': id,
                            'mark': finalgrade,
                            'itemname': item_name,


                        }
                    else:
                        data_to_insert = {
                            'id': id,
                            'mark': float(finalgrade),
                            'itemname': None
                        }
                    mongo_collection.insert_one(data_to_insert)
                else:
                    print(f"Skipping record with id={id} because finalgrade is None")

except mysql.connector.Error as e:
    print(f"Error: {e}")