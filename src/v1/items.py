# own
from orm import Item


# pip
from flask import Blueprint, make_response, request, current_app, jsonify

items_bp = Blueprint("items", __name__)


@items_bp.route("/items/<int:id>", methods=["GET"], endpoint="get_items_from_id")
def get_items_from_id(current_user, id):
    return f"One product: {id}"


@items_bp.route("/items", methods=["POST"], endpoint="post_create_item")
# admin check
def post_create_item():
    data = request.get_json()

    Item.add(**data)

    return make_response("Item created", 201)


@items_bp.route("/items", methods=["GET"], endpoint="get_all_items")
def get_all_items():
    db = current_app.db
    items = db.session.query(Item).all()

    item_data = [{"id": item.id, "name": item.name, "price": item.price, "image": item.img} for item in items]

    return jsonify(item_data)