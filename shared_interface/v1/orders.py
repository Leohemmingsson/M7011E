# own
from permissions import token_required

from task_worker import create_order, get_all_orders, get_order_by_id, get_orders_by_customer_id, get_orders_by_status
# pip
from flask import Blueprint, request, make_response

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["POST"], endpoint="post_create_order")
@token_required
def post_create_order(current_user):

    data=request.get_json()
    data["customer_id"] = current_user["public_id"]

    req = create_order.delay(data)
    response, status_code = req.get()

    return make_response(response, status_code)


@orders_bp.route("/orders/<int:id>", methods=["GET"], endpoint="get_orders_from_id")
@token_required
def get_orders_from_id(current_user, id):
    req = get_order_by_id.delay(id)
    response, status_code = req.get()

    return make_response(response, status_code)

@orders_bp.route("/orders", methods=["GET"], endpoint="get_all_orders")
@token_required
def get_all_orders(current_user):
    req = get_all_orders.delay()
    response, status_code = req.get()

    return make_response(response, status_code)

@orders_bp.route("/orders/customer/<int:id>", methods=["GET"], endpoint="get_orders_by_customer_id")
@token_required
def get_orders_by_customer_id(current_user, id):
    req = get_orders_by_customer_id.delay(id)
    response, status_code = req.get()

    return make_response(response, status_code)

@orders_bp.route("/orders/status/<string:status>", methods=["GET"], endpoint="get_orders_by_status")
@token_required
def get_orders_by_status(current_user, status):
    req = get_orders_by_status.delay(status)
    response, status_code = req.get()

    return make_response(response, status_code)
