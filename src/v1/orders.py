# own
from permissions import token_required

# pip
from flask import Blueprint

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["GET"], endpoint="create_order")
@token_required
def get_all_orders(current_user):
    return "Orders"


@orders_bp.route("/orders/<int:id>", methods=["GET"], endpoint="get_orders_from_id")
@token_required
def get_orders_from_id(current_user, id):
    return f"One order: {id}"
