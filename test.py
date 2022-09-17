import sqlite3

con =sqlite3.connect('data.db')

cursor = con.cursor()

create_table = 'CREATE TABLE users (id int, username text, password text)'

cursor.execute(create_table)

user = (1, 'bob', 'asdf')

insert_query =  "INSERT INTO users VALUES (?,?,?)"

cursor.execute(insert_query,user)


users = [
    (2, 'boba', 'asdaf'),
    (3, 'qaws', 'qqaa')
]

cursor.executemany(insert_query,users)

select_query =  "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)

con.commit()

con.close()
