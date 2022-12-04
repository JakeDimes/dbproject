import sqlite3
from sqlite3 import Error
import sys
import os
def create_connection(database_file):
    """
    Opens the database file, returns database object

    Keyword Arugments
    database_file -- path to the database file
    """

    database = none
    
    try:
        database = sqlite3.connect(database_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
        print("Connection to Database failed")

    return database



def load_queries():
    """
    Reads all queries in the ./src folder and formats them into a dictionary
    """

    # the number of the query
    query_num = 1

    for 


    


def main( ):
    if len(sys.argv) != 2:
        print("Error: Please pass the path to the Bookstore.db file as the first argument to this program. Exiting")
        return

    database = create_connection(sys.argv[1])






if __name__ == '__main__':
    main()

