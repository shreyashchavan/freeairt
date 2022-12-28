import sqlite3

# Connect to the database
conn = sqlite3.connect('mydatabase.db')

# Create a cursor
c = conn.cursor()


import sqlite3

# Connect to the database
conn = sqlite3.connect('mydatabase.db')

# Create a cursor
cursor = conn.cursor()

# Create the schema

cursor.execute('''
    CREATE TABLE reviews(
        name INTEGER NOT NULL,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')

# Commit the changes
conn.commit()

# Close the connection
conn.close()