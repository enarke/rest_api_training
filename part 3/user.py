import sqlite3

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        print(username, password)
    
    @classmethod    
    def find_by_username(self, username):
        con =sqlite3.connect('data.db')
        cursor = con.cursor()
        select_query = "SELECT * FROM users WHERE username = ?"
        result = cursor.execute(select_query,(username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
            
        con.close()
        return user
    
    @classmethod
    def find_by_id(self, id):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        select_query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(select_query, (id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        con.close()
        return user
