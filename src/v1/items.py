# own
from permissions import token_required

# pip
from flask import Blueprint

items_bp = Blueprint("items", __name__)


@items_bp.route("/items", methods=["GET"], endpoint="get_all_items")
@token_required
def get_all_items(current_user):
    return "Products"


@items_bp.route("/items/<int:id>", methods=["GET"], endpoint="get_items_from_id")
@token_required
def get_items_from_id(current_user, id):
    return f"One product: {id}"
