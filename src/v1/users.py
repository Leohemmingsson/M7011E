# std
import uuid

# own
from permissions import token_required, hash_password
from orm import User


# pip
from flask import Blueprint, make_response, request, current_app, jsonify
from sqlalchemy import delete

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"], endpoint="post_create_user")
def post_create_user():
    session = current_app.get("session")
    data = request.get_json()

    data["password"] = hash_password(data["password"])
    data["public_id"] = str(uuid.uuid4())

    new_user = User(**data)

    session.add(new_user)
    session.commit()

    return make_response("User created", 201)


@users_bp.route("/users/confirm/<string:public_id>", methods=["GET"], endpoint="confirm_mail")
def confirm_mail(public_id):
    # sql_activate_user(cursor, public_id)

    return make_response("User activated", 200)


@users_bp.route("/users", methods=["GET"], endpoint="get_all_users")
@token_required
def get_all_users(current_user):
    print("[Warning] Need to check if user is admin")
    session = current_app.get("session")
    users = session.query(User).all()

    users_data = [{"id": user.id, "username": user.username, "email": user.email} for user in users]

    return jsonify(users_data)


@users_bp.route("/users/<int:id>", methods=["GET"], endpoint="get_user_from_id")
@token_required
def get_user_from_id(current_user, id):
    print("[Warning] Need to check if user is admin")
    return f"One user: {id}"


@users_bp.route("/users/<string:username>", methods=["DELETE"], endpoint="remove_user_from_id")
@token_required
def remove_user_from_id(current_user, username):
    print("[Warning] Need to check if user is admin or if the request if from same person")
    delete(User).where(User.username == username).execute()

    return make_response("User deleted", 200)
