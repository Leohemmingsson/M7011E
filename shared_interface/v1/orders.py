# own
from permissions import token_required, is_authorized, AuthorizationLevel as AL

from task_worker import (
    create_order,
    get_all_orders,
    get_order_by_id,
    get_orders_by_customer_id,
    get_uid_on_order,
    mark_order_done,
)

# pip
from flask import Blueprint, make_response

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/orders", methods=["POST"], endpoint="post_create_order")
@token_required
def post_create_order(current_user):
    req = create_order.delay(current_user["public_id"])
    response, status_code = req.get()

    return make_response(response, status_code)


@orders_bp.route("/orders/<int:order_id>/done", methods=["POST"], endpoint="route_mark_order_done")
def route_mark_order_done(order_id: int):
    req = mark_order_done.delay(order_id)
    response, status_code = req.get()

    return make_response(response, status_code)


@orders_bp.route("/orders/<int:id>", methods=["GET"], endpoint="get_orders_from_id")
@token_required
def get_orders_from_id(current_user, order_id):
    req = get_uid_on_order.delay(order_id)
    owner, status_code = req.get()
    if not (
        is_authorized(
            required_permission=AL.ADMIN, user=current_user, allow_user_exeption=True, exception_public_id=owner
        )
    ):
        return make_response("Unauthorized", 401)
    req = get_order_by_id.delay(id)
    response, status_code = req.get()

    return make_response(response, status_code)


@orders_bp.route("/orders", methods=["GET"], endpoint="route_get_all_orders")
@token_required
def route_get_all_orders(current_user):
    if not (is_authorized(required_permission=AL.ADMIN, user=current_user)):
        return make_response("Unauthorized", 401)
    req = get_all_orders.delay()
    response, status_code = req.get()

    return make_response(response, status_code)


@orders_bp.route("/orders/customer/<int:id>", methods=["GET"], endpoint="route_get_orders_by_customer_id")
@token_required
def route_get_orders_by_customer_id(current_user, id):
    req = get_orders_by_customer_id.delay(id)
    response, status_code = req.get()

    return make_response(response, status_code)
