# own
# from permissions import token_required, is_authorized, AuthorizationLevel
from task_worker import (
    get_all_items,
    create_item,
    delete_item_by_id,
    get_item_by_name,
    get_item_by_id,
    update_item_fields,
)


# pip
from flask import Blueprint, make_response, request

items_bp = Blueprint("items", __name__)


@items_bp.route("/items", methods=["POST"], endpoint="post_create_item")
# @token_required
def post_create_item():
    data = request.get_json()

    req = create_item.delay(data)
    response, status_code = req.get()
    return make_response(response, status_code)


@items_bp.route("/items", methods=["GET"], endpoint="route_get_all_items")
# @token_required
def route_get_all_items():
    req = get_all_items.delay()
    resonse, status_code = req.get()
    return make_response(resonse, status_code)


@items_bp.route("/items/<string:name>", methods=["GET"], endpoint="get_items_from_name")
# @token_required
def get_items_from_name(name):
    req = get_item_by_name.delay(name)
    response, status_code = req.get()

    return make_response(response, status_code)


@items_bp.route("/items/<int:id>", methods=["GET"], endpoint="route_get_item_by_id")
# @token_required
def rout_get_item_by_id(id):
    req = get_item_by_id.delay(id)
    response, status_code = req.get()

    return make_response(response, status_code)


@items_bp.route("/items/<int:id>", methods=["DELETE"], endpoint="route_delete_item_by_name")
def route_delete_item_by_name(id):
    req = delete_item_by_id.delay(id)
    response, status_code = req.get()
    return make_response(response, status_code)


@items_bp.route("/items/<int:item_id>", methods=["PUT"], endpoint="route_update_item_fields")
def route_update_item_fields(item_id):
    data = request.get_json()
    req = update_item_fields.delay(item_id, data)
    response, status_code = req.get()

    return make_response(response, status_code)
