from flask import Blueprint

items_bp = Blueprint("items", __name__)


@items_bp.route("/items", endpoint="items")
def items():
    return "Products"


@items_bp.route("/items/<int:id>", endpoint="get_from_id")
def get_from_id(id):
    return f"One product: {id}"
