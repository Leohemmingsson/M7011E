# std
import uuid
import os

# own
from permissions import token_required, hash_password, is_authorized, AuthorizationLevel
from mail import send_confirmation_email
from orm import User


# pip
from flask import Blueprint, make_response, request, jsonify
import yagmail

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"], endpoint="post_create_user")
def post_create_user():
    data = request.get_json()

    data["password"] = hash_password(data["password"])
    data["public_id"] = str(uuid.uuid4())
    data["activated"] = False
    data["type"] = AuthorizationLevel.CUSTOMER.name
    # data["type"] = AuthorizationLevel.ADMIN.name
    # data["type"] = AuthorizationLevel.SUPERUSER.name

    if "mail" not in data:
        return make_response("Mail is missing", 400)

    new_user = User.add(**data)

    send_confirmation_email(new_user)

    return make_response("User created", 201)


@users_bp.route("/users", methods=["GET"], endpoint="get_all_users")
@token_required
def get_all_users(current_user):
    if not is_authorized(current_user, AuthorizationLevel.ADMIN):
        return make_response("Unauthorized", 401)

    users = User.get_all()
    users_data = [one_user.to_dict for one_user in users]

    return jsonify(users_data)


@users_bp.route("/users/confirm/<string:public_id>", methods=["GET"], endpoint="confirm_mail")
def confirm_mail(public_id):
    statement = User.public_id == public_id
    user_to_confirm = User.get_first_where(statement)

    if not user_to_confirm:
        return make_response("User not found", 404)

    user_to_confirm.update("activated", True)

    return make_response("Mail confirmed", 200)


@users_bp.route("/users/<string:username>", methods=["GET"], endpoint="get_user_from_username")
@token_required
def get_user_from_username(current_user, username):
    if not (is_authorized(current_user, only_higher_than_user=True, exception_username=username)):
        return make_response("Unauthorized", 401)

    statement = User.username == username
    user = User.get_first_where(statement)

    if not user:
        return make_response("User not found", 404)

    return jsonify(user.to_dict)


@users_bp.route("/users/<string:username>", methods=["DELETE"], endpoint="remove_user_from_username")
@token_required
def remove_user_from_username(current_user, username):
    if not (is_authorized(current_user, only_higher_than_user=True, exception_username=username)):
        return make_response("Unauthorized", 401)

    statement = User.username == username
    User.delete_where(statement)

    return make_response("User deleted", 200)


@users_bp.route("/users/<string:username>", methods=["PUT"], endpoint="update_user_fields")
@token_required
def update_user_fields(current_user, username):
    if not (is_authorized(current_user, only_higher_than_user=True, exception_username=username)):
        return make_response("Unauthorized", 401)

    data = request.get_json()
    statement = User.username == username
    user = User.get_first_where(statement)

    if not user:
        return make_response("User not found", 404)

    for key, value in data.items():
        user.update(key, value)

    return make_response("User updated", 200)
