from flask import Flask, request
from db import stores
import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import items

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
       try:
          return items[item_id]
       except KeyError:
          abort(404, message="Item not found")
    
    def delete(self, item_id):
       try:
          del items[item_id]
          return {"message": "Item deleted"}
       except KeyError:
          abort(400, message="Item does not exist")
    
    def put(self, item_id):
        item_data = request.get_json()
        
        if "price" not in item_data or "name" not in item_data:
            abort(
            400,
            message="Bad request. Ensure 'price', and 'name' are included in the JSON payload.",
        )
        try:
           item = items[item_id]
           item |= item_data
           return item
        except KeyError:
           abort(404, message="Item not found")
           


@blp.route("/item/<string:item_id>")
class ItemList(MethodView):
    
    def get(self):
        return {"items": list(items.values())}
    
    def post(self):
        item_data = request.get_json()
        if (
        "price" not in item_data
        or "store_id" not in item_data
        or "price" not in item_data
        ):
           abort(400, 
               message="Bad request. Ensure 'price' 'store_id' and 'price' are included in your request"
                )
        for item in items.values():
           if (
              item["name"] == item_data["names"]
              and  item["store_id"] == item_data["store_id"]
           ):
              abort(400, message="Item already exists")        
        
        if item_data["store_id"] not in stores:
           abort(404, message="store not found")
    
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
    
        return item