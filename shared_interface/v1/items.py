# own
# from permissions import token_required, is_authorized, AuthorizationLevel
from task_worker import get_all_items, create_item, get_item_by_id


# pip
from flask import Blueprint, make_response, request

items_bp = Blueprint("items", __name__)


@items_bp.route("/items", methods=["POST"], endpoint="post_create_item")
# @token_required
def post_create_item():
    data = request.get_json()

    req = create_item.delay(data)
    response, status_code = req.get()
    return make_response(f"Item created: {response}", status_code)


@items_bp.route("/items", methods=["GET"], endpoint="route_get_all_items")
# @token_required
def route_get_all_items():
    req = get_all_items.delay()
    resonse, status_code = req.get()
    return make_response(resonse, status_code)


@items_bp.route("/items/<int:id>", methods=["GET"], endpoint="get_items_from_id")
# @token_required
def get_items_from_id(id):
    req = get_item_by_id.delay(id)
    response, status_code = req.get()

    return make_response(response, status_code)


@items_bp.route("/items/<int:id>", methods=["GET"], endpoint="update_item_fields")
# @token_required
def update_item_fields(id):
    # if not (is_authorized(current_user, AuthorizationLevel.ADMIN)):
    #     return make_response("Unauthorized", 401)

    raise NotImplementedError("Not implemented yet")


@items_bp.route("/items/<int:id>", methods=["DELETE"], endpoint="delete_item_by_id")
def delete_item_by_id(id):
    req = delete_item_by_id.delay(id)
    response, status_code = req.get()
    return make_response(response, status_code)
