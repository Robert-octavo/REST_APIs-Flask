import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item
        """
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Store not found")
        """

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)

        db.session.add(item)
        db.session.commit()
        return item
        # item_data = request.get_json()
        """
        try:
            item = items[item_id]
            item |= item_data  # Update the item dictionay with the info in the item_data
        except KeyError:
            abort(404, message="Item not found.")
        """

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}, 200

        #raise NotImplementedError("Deleting an item is not implemented.")
        """
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found")
        """


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
        # return {"items": list(items.values())}

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error ocurred while inserting the item.")

        return item
        # item_data = request.get_json() it's send from the schema
        """
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
        """
