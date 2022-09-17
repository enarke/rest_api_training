from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)

api = Api(app)

items = []

class Item(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Thi s field cannot be blank"
                        )
        
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items),None)
            
        return {'Item':item}, 200 if item is not None else 400
    
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message' : "A item with the name '{}' already exists".format(name)}, 400
        
        data = Item.parser.parse_args()
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201
    
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return  {'message': "A item with the name '{}' deleted".format(name)}, 200
    
    def put(self, name):
        
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {
                'name': name,
                'price': data['price']
            }
            items.append(item)
            return item, 201
        else:
            
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'items':items}        
    
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


app.run(port = 5000, debug = True)

