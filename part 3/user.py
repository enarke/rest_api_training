import sqlite3
from flask_restful import Resource, reqparse

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    @classmethod       
    def find_by_username(cls, username):
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
    def find_by_id(cls, id):
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

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="username field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="password field cannot be left blank!"
                        )
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if User.find_by_username(data["username"]):
            return {'message': 'username already exists'}, 400
        
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        
        insert_query =  "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(insert_query,(data['username'],data['password']))
                
        con.commit()
        con.close()
        
        return {'message': "An user added succesfully."},201