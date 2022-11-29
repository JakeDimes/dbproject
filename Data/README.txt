To load the data into the database, complete the following seteps.

Please note, the commands where issued on a GNU+Linux system. The '$' designates a bash command prompt.

(1) Ensure the Sqlite3 is installed and accessible. On Arch based systems:

	$ sudo pacman -S sqlite3

(2) Create the database file by running:

	$ sqlite3 /desired/save/path/Bookstore.db

(3) Exit the sqlite3 command prompt:

	sqlite3> .exit

(4) Load the Schema:

	$ sqlite3 /desired/save/path/Bookstore.db < /submission/Create/BookStoreDB.txt

(5) Load the Data:

	$ sqlite3 /desired/save/path/Bookstore.db < /submission/Data/DefaultData.txt
