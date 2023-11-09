# own
from orm import Item
from permissions import token_required, is_authorized, AuthorizationLevel

# pip
from flask import Blueprint, make_response, request, current_app, jsonify

items_bp = Blueprint("items", __name__)


@items_bp.route("/items", methods=["POST"], endpoint="post_create_item")
@token_required
def post_create_item():
    data = request.get_json()
    Item.add(**data)
    return make_response("Item created", 201)


@items_bp.route("/items", methods=["GET"], endpoint="get_all_items")
@token_required
def get_all_items():
    items = Item.get_all()
    items = [one_item.to_dict for one_item in items]
    return jsonify(items)


@items_bp.route("/items/<int:id>", methods=["GET"], endpoint="get_items_from_id")
@token_required
def get_items_from_id(current_user, id):
    statement = Item.id == id
    item = Item.get_first_where(statement)

    if not item:
        return make_response("Item not found", 404)

    return jsonify(item.to_dict)


@items_bp.route("/items/<int:id>", methods=["GET"], endpoint="update_item_fields")
@token_required
def update_item_fields(current_user, id):
    if not (is_authorized(current_user, AuthorizationLevel.ADMIN)):
        return make_response("Unauthorized", 401)

    data = request.get_json()
    statement = Item.id == id
    item = Item.get_first_where(statement)

    if not item:
        return make_response("Item not found", 404)

    for key, value in data.items():
        item.update(key, value)

    return make_response("User updated", 200)
