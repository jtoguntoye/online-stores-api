from flask import Flask, request
from db import stores

import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from schemas import ItemSchema, ItemUpdateSchema

from db import items

blp = Blueprint("Items", __name__, description="Operations on items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    
    @blp.response(200, ItemSchema)   
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
    
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
           item = items[item_id]
           item |= item_data
           
           return item
        except KeyError:
           abort(404, message="Item not found")
           


@blp.route("/item/<string:item_id>")
class ItemList(MethodView):
    
    
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
     
     
     
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
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
     
     
from db import db

class ItemModel(db.Model):
   __tablename__ = "items"
   
   id  = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(80), unique=True, nullable=False)
   price = db.Column(db.Float(precision=2), unique=False, nullable=False)
   
   store_id = db.Column(db.Integer, db.ForeignKey("stores.id"),unique=False, nullable=False)
   store = db.relationship("StoreModel", back_populates="items")
   