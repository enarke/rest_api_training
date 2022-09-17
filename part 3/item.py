import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import  jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        
        item = self.find_by_name(name)
        if item:
            return item, 200
        return {'message': 'item not found'}, 401
    @classmethod
    def find_by_name(cls, name):
        con =sqlite3.connect('data.db')
        cursor = con.cursor()
        
        select_query = "SELECT * FROM items WHERE name = ?"
        result = cursor.execute(select_query,(name,))
        row = result.fetchone()
        con.close()

        if row:
            return {'item': {'name':row[0], 'price': row[1]}}
        return None
    
    @classmethod
    def insert(cls, item):
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        insert_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(insert_query, (item['name'], item['price']))
        con.commit()

    def post(self, name):
        
        if self.find_by_name(name):
            print("An item with name '{}' already exists.".format(name))
            return {'message': "An item with name '{}' already exists.".format(name)}

        data = Item.parser.parse_args()
        item = { 'name': name, 'price': data['price']}
        
        try:
            self.insert(item)
        except:
            return {'message': "An item with name '{}' unable to insert.".format(name)}, 500
            
        
        return {'message': "An item with name '{}' and price '{}' added.".format(name, data['price'])}

    @jwt_required()
    def delete(self, name):
        
        if not self.find_by_name(name):
            print("An item with name '{}' does not exists.".format(name))
            return {'message': "An item with name '{}' does not exists.".format(name)}
        
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        insert_query =  "DELETE FROM items WHERE name = ?"
        cursor.execute(insert_query,(name,))
        con.commit()
        
        return {'message': "An item with name '{}' deleted.".format(name,)}
        
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        con =sqlite3.connect('data.db')
        cursor = con.cursor()
        
        select_query = "SELECT * FROM items"
        result = cursor.execute(select_query)
        items = result.fetchall()
        con.close()
        return {'items': items}
