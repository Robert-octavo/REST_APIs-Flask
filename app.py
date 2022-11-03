import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items, stores


app = Flask(__name__)


@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()

    # check if the name exist in the payload
    if "name" not in store_data:
        abort(
            400,
            message="Bad request. Ensure 'name' is included in the JSON payload"
        )

    # check if the store exists
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="Store already exists.")

    # create a new store and add a id
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post("/item")  # Get the id_store in the payload
def create_item():
    item_data = request.get_json()
    # check if all elements are included in the payload
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request, All element have to be included in the payload"
        )

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


@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")


@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Store not found")


@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found")


@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found")


@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400, message="Bad request, Ensure the price and name exists in the payload")
    try:
        item = items[item_id]
        item |= item_data  # Update the item dictionay with the info in the item_data
    except KeyError:
        abort(404, message="Item not found.")


@app.get("/item")
def get_items():
    return {"items": list(items.values())}
