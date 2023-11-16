# own
# from permissions import token_required, is_authorized, AuthorizationLevel
from task_worker import get_all_items, create_item, delete_item_by_name, get_item_by_name


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


@items_bp.route("/items/<int:id>", methods=["GET"], endpoint="get_item_by_id")
# @token_required
def get_item_by_id(id):
    req = get_item_by_id.delay(id)
    response, status_code = req.get()

    return make_response(response, status_code)


@items_bp.route("/items/<string:name>", methods=["GET"], endpoint="update_item_fields")
# @token_required
def update_item_fields(name):
    # if not (is_authorized(current_user, AuthorizationLevel.ADMIN)):
    #     return make_response("Unauthorized", 401)

    raise NotImplementedError("Not implemented yet")


@items_bp.route("/items/<string:name>", methods=["DELETE"], endpoint="route_delete_item_by_name")
def route_delete_item_by_name(name):
    req = delete_item_by_name.delay(name)
    response, status_code = req.get()
    return make_response(response, status_code)
