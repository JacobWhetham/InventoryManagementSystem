"""
    :author:        Jacob Whetham
    :version:       1.0.0, 04 JAN 2024
    :desc:          This file holds the driving function of the program.
"""

# Imports
import inventory_management_frontend as imf     # Allows for use of the frontend of the Inventory Management System.
import pymongo                                  # Allows for use of MongoDB functionality.

# Declare Global Variables
#   The username and password are initially used to create a user for the database. This allows testing
#       the user authentication system.
username = "user"                                       # The username to use in accessing the database.
password = "password"                                   # The password to use in accessing the database.
host = "localhost"                                      # The host to use in accessing the database.
port = 27017                                            # The port to use in accessing the database.
target_db = "inventory_management_db"                   # The database to be used.
target_collection = "inventory_management_collection"   # The collection to be used.


def start():
    """
        Populates the database with data if needed before starting the frontend service.
    """
    # The below code accesses the admin account of the MongoClient.
    client = pymongo.MongoClient(f"mongodb://{host}:{port}/")  # Connects to the MongoDB client as an admin.
    database = client['admin']  # Accesses the 'admin' database within the MongoDB client.
    collection = database['system.users']  # Accesses the collection for the users in the database.

    # If the user is not yet registered in the admin database,
    if len(list(collection.find({'user': username}))) == 0:
        database.command("createUser", username, pwd=password,
                         roles=[{"role": "readWrite", "db": target_db}])  # Adds the user to the database.

    client.close()  # Closes the client (prevents admin-level access for future operations).

    # The below code logs into the target database as the generated user.
    client = pymongo.MongoClient(
        f"mongodb://{username}:{password}@{host}:{port}/")  # Logs in to the MongoDB client as the user.
    database = client[target_db]  # Forges a reference to the targeted database.
    collection = database[target_collection]  # Forges a reference to the collection within the targeted database.

    # If the targeted collection does not yet exist,
    if target_collection not in database.list_collection_names():
        to_insert = []   # Holds the entries to be inserted into the database.

        # For 100 entries,
        for i in range(100):
            to_insert.append({"product_id": i,
                             "product_name": "",
                             "product_price": 0,
                             "product_quantity": 0})  # Appends a dict containing the data to be added to the list.

        collection.insert_many(to_insert)  # Inserts every entry in the list to the database.

    client.close()  # Closes the connection to the MongoDB client.
    imf.start()  # Starts the frontend of the Inventory Management System (creates the dashboard).


# The below code runs as soon as the program starts.
if __name__ == "__main__":
    start()  # Starts the frontend service.


