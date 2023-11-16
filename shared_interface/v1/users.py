# std
import logging

# own
from permissions import token_required, hash_password, is_authorized, AuthorizationLevel
from task_worker import (
    get_all_users,
    create_user,
    delete_user_by_username,
    get_user_by_username,
    activate_user_by_public_id,
    update_user_cloumns,
)

from mail import send_confirmation_email


# pip
from flask import Blueprint, make_response, request, jsonify

users_bp = Blueprint("users", __name__)
logging.basicConfig(level=logging.INFO)


@users_bp.route("/users", methods=["POST"], endpoint="post_create_user")
def post_create_user():
    data = request.get_json()
    data["password"] = hash_password(data["password"])
    data["type"] = AuthorizationLevel.CUSTOMER.name

    if "mail" not in data:
        return make_response("Mail is missing", 400)

    req = create_user.delay(data)

    response, status_code = req.get()

    if status_code == 201:
        new_user = response
        send_confirmation_email(new_user)

    return make_response(f"User created: {response}", status_code)


@users_bp.route("/users", methods=["GET"], endpoint="route_get_all_users")
@token_required
def route_get_all_users(current_user):
    if not is_authorized(current_user, AuthorizationLevel.ADMIN):
        return make_response("Unauthorized", 401)

    req = get_all_users.delay()
    all_users: list = req.get()

    return jsonify(all_users)


@users_bp.route("/users/confirm/<string:public_id>", methods=["GET"], endpoint="confirm_mail")
def confirm_mail(public_id):
    req = activate_user_by_public_id.delay(public_id)
    response, status_code = req.get()

    return make_response(response, status_code)


@users_bp.route("/users/<string:username>", methods=["GET"], endpoint="get_user_from_username")
@token_required
def get_user_from_username(current_user, username):
    if not (
        is_authorized(current_user, only_higher_than_user=True, allow_user_exeption=True, exception_username=username)
    ):
        return make_response("Unauthorized", 401)

    req = get_user_by_username.delay(username)
    response, status_code = req.get()

    return make_response(jsonify(response), status_code)


@users_bp.route("/users/<string:username>", methods=["DELETE"], endpoint="remove_user_with_username")
@token_required
def remove_user_with_username(current_user, username):
    if not (
        is_authorized(current_user, only_higher_than_user=True, allow_user_exeption=True, exception_username=username)
    ):
        return make_response("Unauthorized", 401)

    req = delete_user_by_username.delay(username)
    response, status_code = req.get()

    return make_response(response, status_code)


@users_bp.route("/users/<string:username>", methods=["PUT"], endpoint="update_user_fields")
@token_required
def update_user_fields(current_user, username):
    if not (
        is_authorized(current_user, only_higher_than_user=True, allow_user_exeption=True, exception_username=username)
    ):
        return make_response("Unauthorized", 401)

    data = request.get_json()
    if "password" in data and data["password"]:
        data["password"] = hash_password(data["password"])

    req = update_user_cloumns.delay(username, data)
    response, status_code = req.get()

    return make_response(response, status_code)
