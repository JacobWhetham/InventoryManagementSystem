"""
    :author:        Jacob Whetham
    :version:       1.0.0, 04 JAN 2024
    :desc:          This file handles the backend of the Inventory Management System (MongoDB).
"""

# Imports
import pandas       # Allows for Pandas functionality e.g. creating DataFrames.
import pymongo      # Allows for the use of MongoDB.

# Declare global variables.
client : pymongo.MongoClient = None                         # The reference to the MongoClient connection.
database = None                                             # The database to be used.
collection = None                                           # The collection to be used in the database.
logged_in = False                                           # Whether a connection is held to the MongoClient.
target_db = "inventory_management_db"                       # The database to use.
target_collection = "inventory_management_collection"       # The collection to use.


def login(username, password):
    """
        Forges the connection to the MongoClient.

        :param username:        The username to use in forging the connection.
        :param password:        The password to use in forging the connection.
    """

    # Declare which variables use the global scope.
    global client, collection, database, logged_in

    # Makes an attempt,
    try:
        # Forges the connection to the MongoClient
        client = pymongo.MongoClient(host="localhost", port=27017, username=username, password=password,
                                     serverSelectionTimeoutMS=1)

        # The below line is used to throw an error if the connection could not be forged.
        #   This ensures the connection is valid before accessing the database.
        client.server_info()  # Gets info from the server.

        database = client[target_db]  # Gets a reference to the target database.
        collection = database[target_collection]  # Gets a reference to the target collection.
        logged_in = True  # Updates the login status (login succeeded).

    # If an error occurred,
    except Exception:
        logged_in = False  # Updates the login status (login failed).


def logout():
    """
        Closes the connection to the MongoClient.
    """

    # Declare which variables use the global scope.
    global client, collection, database, logged_in

    # Makes an attempt,
    try:
        client.close()  # Closes the connection to the MongoClient.
        logged_in = False  # Updates the login status (logout succeeded).

    # If an error occurred,
    except Exception:
        print("The connection could not be closed!")  # Outputs an error.


def create(data : dict ={}):
    """
        Creates a new entry in the database.

        :param data:    The data to be used in creating the new entry.
    """

    # If the user is not logged in,
    if not logged_in:
        print("Login first!")  # Output an error
        return  # Exit the function (the user should not be able to create entries if they aren't logged in).

    # The below code only runs if the user is logged in.

    # Makes an attempt,
    try:
        collection.insert_one(data)  # Creates a new document in the collection.

    # If an error occurred,
    except Exception:
        print("The insertion failed.")  # Outputs an error.


def read(query : dict ={}) -> pymongo.CursorType:
    """
        Reads data from the collection.

        :param query:               The dictionary to be used to find the matching documents.
        :return CursorType:         The cursor (result) of the search.
    """

    # If the user is not logged in,
    if not logged_in:
        print("Login first!")  # Outputs an error.
        return None  # Returns nothing (the user should not be able to retrieve data unless they are logged in).

    # The below code only runs if the user is logged in.

    results = collection.find(query)  # Stores the results of the search.
    return results  # Returns the results of the search.


def update(query : dict ={}, data : dict ={}):
    """
        Updates one entry with new data.

        :param query:       A dictionary containing an identifier of the entry to update.
        :param data:        A dictionary of the new data to apply to the found entry.
    """

    # If the user is not logged in,
    if not logged_in:
        print("Login first!")  # Outputs an error.
        return  # Exits the function (the user should not be able to update the entries unless they are logged in).

    # The below code only runs if the user is logged in.

    # Makes an attempt,
    try:
        collection.update_one(query, data)  # Updates the entry with new data.

    # If an error occurred,
    except Exception:
        print("The document could not be updated!")  # Outputs an error.


def delete(query : dict):
    """
        Deletes an entry from the database.

        :param query:   A dictionary containing an identifier for the document to be deleted.
    """

    # If the user is not logged in,
    if not logged_in:
        print("Login first!")  # Outputs an error.
        return  # Exits the function (the user should not be able to delete documents unless they are logged in).

    # The below code only executes if the user is logged in.

    # If the query is empty,
    if (query == None or query == {}):
        print("Specify something to delete!")  # Output an error.
        return  # Exits the function (specifying nothing would delete the first entry in the database).

    # The below code only executes if the query is not empty.

    # Makes an attempt,
    try:
        collection.delete_one(query)  # Deletes the entry found with the query.

    # If an error is occurred,
    except Exception:
        print("The document could not be deleted!")  # Outputs an error.


def get_data_frame(cursor : pymongo.CursorType) -> pandas.DataFrame:
    """
        Gets a DataFrame from a cursor (search result).

        :param cursor:              The cursor (result) of a database search.
        :return DataFrame:          The DataFrame created.
    """

    df = pandas.DataFrame.from_records(cursor)  # Creates a DataFrame from the cursor.
    return df  # Returns the DataFrame.


def convert_dataframe_to_dict(df : pandas.DataFrame) -> dict:
    """
        Converts the specified DataFrame to a dictionary.

        :param df:          The DataFrame to convert.
        :return dict:       The dictionary created from the DataFrame.
    """

    # If the DataFrame contains an "_id" column:
    if "_id" in df.columns:
        df.drop("_id", axis=1, inplace=True)  # Drops the "_id" column from the DataFrame.

    # Otherwise (the DataFrame does not have an "_id" column):
    else:
        print("_id was not found!")  # Outputs an error.

    return df.to_dict("records")  # Returns a dictionary created from the DataFrame.


def deleteDatabase():
    """
        Deletes the database and generated user. This cleans up everything that was created by the program.
    """
    # Declare the global scope variables.
    global client, collection, database, logged_in

    # If the user is not logged in,
    if not logged_in:
        print("Please login first!")  # Outputs an error.
        return  # Exits the function (the user should only be able to drop the database if they are logged in).

    username_to_delete = "user"  # Defines the username to delete.

    client.drop_database(target_db)  # Drops the target database.
    client.close()  # Closes the connection to the MongoClient.

    client = pymongo.MongoClient("mongodb://localhost:27017")  # Forges a new connection as the admin to the MongoClient.
    database = client["admin"]  # Uses the admin database.
    collection = database["system.users"]  # Uses the system.users collection.
    database.command("dropUser", username_to_delete)  # Drops the specified user.
    client.close()  # Closes the connection to the MongoClient.
