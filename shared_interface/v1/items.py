# own
from permissions import token_required, is_authorized, AuthorizationLevel
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
@token_required
def post_create_item(current_user):
    """
    Create item.
    body:
    {
        "name": str,
        "price": int,
        "in_stock": int (TRUE/FALSE),
        "image": str,
    }
    Authorizationlevel: ADMIN
    """
    if not is_authorized(current_user, AuthorizationLevel.ADMIN):
        return make_response("Unauthorized", 401)

    data = request.get_json()

    req = create_item.delay(data)
    response, status_code = req.get()
    return make_response(response, status_code)


@items_bp.route("/items", methods=["GET"], endpoint="route_get_all_items")
def route_get_all_items():
    """
    Everyone can see items, no token required.
    """
    req = get_all_items.delay()
    resonse, status_code = req.get()
    return make_response(resonse, status_code)


@items_bp.route("/items/<string:name>", methods=["GET"], endpoint="get_items_from_name")
def get_items_from_name(name):
    """
    Everyone can see items, no token required.
    """
    req = get_item_by_name.delay(name)
    response, status_code = req.get()

    return make_response(response, status_code)


@items_bp.route("/items/<int:id>", methods=["GET"], endpoint="route_get_item_by_id")
def route_get_item_by_id(id):
    """
    Everyone can see items, no token required.
    """
    req = get_item_by_id.delay(id)
    response, status_code = req.get()

    return make_response(response, status_code)


@items_bp.route("/items/<int:id>", methods=["DELETE"], endpoint="route_delete_item_by_name")
@token_required
def route_delete_item_by_name(current_user, id):
    """
    Delete item by id.
    Authorizationlevel: ADMIN
    """
    if not is_authorized(current_user, AuthorizationLevel.ADMIN):
        return make_response("Unauthorized", 401)

    req = delete_item_by_id.delay(id)
    response, status_code = req.get()
    return make_response(response, status_code)


@items_bp.route("/items/<int:item_id>", methods=["PUT"], endpoint="route_update_item_fields")
@token_required
def route_update_item_fields(current_user, item_id):
    """
    Update existing item.
    Authorizationlevel: ADMIN
    """
    if not is_authorized(current_user, AuthorizationLevel.ADMIN):
        return make_response("Unauthorized", 401)

    data = request.get_json()
    req = update_item_fields.delay(item_id, data)
    response, status_code = req.get()

    return make_response(response, status_code)
