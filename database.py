#Source: https://www.freecodecamp.org/news/connect-python-with-sql/

#Importing libraries
import mysql.connector
from mysql.connector import Error
import pandas as pd

pw = "Project123"

#Connecting to MySQL Server
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_server_connection("localhost", "root", pw)

#Creating a new database
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

#Defining query to create a database and calling the dunction
create_database_query = "CREATE DATABASE chatapp"
create_database(connection, create_database_query)




