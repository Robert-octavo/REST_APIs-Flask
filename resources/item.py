import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Store not found")

    @blp.arguments(ItemUpdateSchema)
    def put(self, item_data, item_id):
        # item_data = request.get_json()

        try:
            item = items[item_id]
            item |= item_data  # Update the item dictionay with the info in the item_data
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found")


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    @blp.arguments(ItemSchema)
    def post(self, item_data):
        # item_data = request.get_json() it's send from the schema

        # check if the item already exists
        for item in items.values():
            if (
                item_data["name"] == item["name"]
                and item_data["store_id"] == item["store_id"]
            ):
                abort(400, message="Item already exists.")

        # check if the store exists
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found")

        # create a new item with the info in the payload and create a unique id
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201
