import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items

app = Flask(__name__)

@app.get("/store")
def get_stores():
    return {"stores": list(stores.values())}, 200

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store with store_id '{}' not found.".format(store_id))
     
@app.get("/item")
def get_items():
    return {"items": list(items.values())}, 200

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except:
        abort(404, message="Item with item_id '{}' not found.".format(item_id))  

@app.post("/store")
def create_store():
    store_data = request.get_json()
    
    if "name" not in store_data:
        abort(400, message="Bad request. Ensure that 'name' is included in the JSON payload.")

    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="A store with the name {} already excists".format(store_data["name"]))
    
    store_id = uuid.uuid4().hex
    store = { **store_data, "id": store_id }
    stores[store_id] = store

    return store, 201

@app.post("/item")
def create_item():
    item_data = request.get_json()

    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(400, message="Bad request ensure that 'store_id', 'name' and 'price' are included in the JSON payload")

    for item in items.values():
        if (
            item_data["name" == item["name"]]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message="Item {} already excist for store_id {}.".format(item["name"], item["store_id"]))

    if item_data["store_id"] not in stores:
        abort(404, message="Store with store_id: '{}' not found.".format(item_data["store_id"]))

    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201