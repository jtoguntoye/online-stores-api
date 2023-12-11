from flask import Flask, request
from db import stores
import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint

blp = Blueprint("stores", __name__, description="Operations on Stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
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
    def get(self):
        return {"stores": list(stores.values())}
    
    def post(self):
        store_data = request.get_json()
        if ("name" not in store_data):
            abort(
            400,
            message="Bad request. Ensure 'name' is included in the store data entered"
            )
    
        for store in stores.values():
           if store_data["name"] == store["name"]:
               abort(400, message="Store already exists") 
        # create unique id for each store
        store_id =  uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
    
        return store, 201
