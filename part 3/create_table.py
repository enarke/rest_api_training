import sqlite3

con =sqlite3.connect('data.db')

cursor = con.cursor()

create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)'
cursor.execute(create_table)

create_table = 'CREATE TABLE IF NOT EXISTS items (name text, price real)'
cursor.execute(create_table)

insert_query =  "INSERT INTO items VALUES (?,?)"
cursor.execute(insert_query,('test','9.99'))
                
con.commit()

con.close()