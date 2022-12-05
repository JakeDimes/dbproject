import sqlite3
from sqlite3 import Error
import sys
import os
from simple_term_menu import TerminalMenu
from tabulate import tabulate

class SavedQuery():
    """
    Object for a query, which stores the SQL code, name, and the description
    """
    def __init__(self, description, code, name):
        self.code = code
        self.name = name
        self.description = description
        


def create_connection(database_file):
    """
    Opens the database file, returns database object

    Keyword Arugments
    database_file -- path to the database file
    """

    database = None
    
    try:
        database = sqlite3.connect(database_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
        print("Connection to Database failed")
        exit()

    return database



def load_queries():
    """
    Reads all queries in the ./src folder and formats them into a dictionary
    """
    
    # will hold Savedquery objects
    queries = dict()
    
    # the number of the query
    query_num = 1

    # get src directory
    walk_dir = './src/'
    walk_dir = os.path.abspath(walk_dir)

    # get all files in the ./src/ directory
    for root, subdirs, files in os.walk(walk_dir):
        files.sort(reverse=True)
        # for all files in the ./src/ directory
        for file in files:

            
            fo = open(os.path.join(root, file))
            
            # save the description, name, and code for a query
            desc = ''
            code = ''
            name = ''

            # state of the read
            flag = 0
            
            # for every line in the file
            for line in fo:

                # look for -- comment markers. Find one = new query
                if flag == 0 and line[0:2] == '--':
                    flag = 1
                # Next -- is the name
                elif flag == 1 and line[0:6] != 'SELECT':
                    name = line
                    flag = 2
                # all subsequent -- comment markets are a description
                elif flag == 2 and line[0:6] != 'SELECT':
                    desc += line

                # the SELECT statement indicates the start of a Query
                elif line[0:6] == 'SELECT' or flag == 3:
                    flag = 3
                    code += line

                    # semicolmn means the end of the query
                    if ';' in line:
                        # now look for a new query
                        flag = 0

                        # save the query
                        queries[query_num] = SavedQuery(desc, code, name)

                        query_num += 1

                        # reset the saved info
                        desc = ''
                        name = ''
                        code = ''

            fo.close()

    return queries
    
def create_entries(queries_dict):
    """
    Creates entries for the menu based on the query description and its number

    Keyword Arugments
    queries_dict -- the dictionary of the queries 
    """
    options = ['Go Back']
    for query_num in queries_dict:
        name = str.rstrip(queries_dict[query_num].name) 

        options.append(f'[{query_num}] {name}')

    return options

def perform_query(database, query_to_perform):
    """
    This performs the query specified on the database

    Keyword Arugments
    database -- the database object
    query_to_perform -- the SQL code for a query as a string
    
    """
    # start a new query 
    loc = database.cursor()
    
    # execute query
    loc.execute(query_to_perform)
    
    # parse the header
    header_orig = loc.description
    header = []
    for tupe in header_orig:
        header.append(tupe[0])


    # get the results from the query
    results = loc.fetchall()

    print(tabulate(results, headers=header, tablefmt='orgtbl'))

    print("\n")

def main( ):
    if len(sys.argv) != 2:
        print("Error: Please pass the path to the Bookstore.db file as the first argument to this program. Exiting")
        return

    database = create_connection(sys.argv[1])

    queries_dict = load_queries()

    # create the menu
    main_menu = TerminalMenu(['See Queries', 'See Views', 'Exit Program'],
                             title='Options')
    query_menu = TerminalMenu(create_entries(queries_dict),
                              title='Queries')
    view_options = ["Go Back", "Author's Most Popular Book",
                                                "Employee Book Quantity Sales", 
                                                "Number of Books in stock for Publishers"]
    view_menu = TerminalMenu(view_options, title="Views")

    
    print('Use the UP/DOWN, or K/J to move up and down the menu. Use ENTER to confirm your selection')
    # prompt the user
    run = True

    while run:

        usr_in = main_menu.show()

        if usr_in == 2:
            print("Exiting Program")

            run = False

        elif usr_in == 1:

            os.system('cls' if os.name == 'nt' else 'clear')
            usr_in = view_menu.show()
            if usr_in != 0:
                print(view_options[usr_in])
                print("\n")

                # find the view
                view_name = "Most_Popular"

                if usr_in == 2:
                    view_name = 'Employee_Sales'
                elif usr_in == 3:
                    view_name = 'Publisher_Stock'

                perform_query(database, f"SELECT * FROM {view_name};") 

        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            usr_in = query_menu.show()
            if usr_in != 0: 
                print(f"Performing Query {usr_in}\n")
                query_to_perform = queries_dict[usr_in]
                print(query_to_perform.description + '\n')

                perform_query(database, query_to_perform.code)

if __name__ == '__main__':
    main()

