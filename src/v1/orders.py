# own
from orm import Order
from permissions import token_required

# pip
from flask import Blueprint, make_response, request, jsonify

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["POST"], endpoint="post_create_order")
@token_required
def post_create_order(current_user):  # lägga till authorization
    data = request.get_json()
    Order.add(current_user, **data)
    return make_response("Order created", 201)


@orders_bp.route("/orders", methods=["GET"], endpoint="get_all_orders")
@token_required
def get_all_orders(current_user):
    orders = Order.get_all()
    orders = [one_order.to_dict for one_order in orders]
    return jsonify(orders)


@orders_bp.route("/orders/<int:id>", methods=["GET"], endpoint="get_order_from_id")
@token_required
def get_order_from_id(current_user, id):
    statement = Order.id == id
    order = Order.get_first_where(statement)

    if not order:
        return make_response("Order not found", 404)

    return jsonify(order.to_dict)
