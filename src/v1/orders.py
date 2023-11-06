from flask import Blueprint

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders")
def orders():
    return "Orders"


@orders_bp.route("/orders/<int:id>")
def get_from_id(id):
    return f"One order: {id}"
