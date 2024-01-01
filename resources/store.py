from flask import Flask, request
from db import stores
import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on Stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(201, StoreSchema)
    def get(self, store_id):
        try:
           return stores[store_id]
        except KeyError:
           abort(404, message="Store not found.")


    def delete(self, store_id):
        try:
           del stores[store_id]
           return {"message": "Store deleted."}
        except KeyError:
           abort(404, message="Store not found.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(cls):
        return {"stores": list(stores.values())}
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(cls, store_data):
        
        for store in stores.values():
           if store_data["name"] == store["name"]:
               abort(400, message="Store already exists") 
        # create unique id for each store
        store_id =  uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
    

        return store

   
from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)