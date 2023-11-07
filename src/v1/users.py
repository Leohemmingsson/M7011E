# std
import uuid

# own
from permissions import token_required, hash_password
from orm import User
from connections import send_confirmation_mail

# pip
from flask import Blueprint, make_response, request, current_app, jsonify

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"], endpoint="post_create_user")
def post_create_user():
    db = current_app.db
    data = request.get_json()

    data["password"] = hash_password(data["password"])
    data["public_id"] = str(uuid.uuid4())
    data["activated"] = 0

    new_user = User(**data)

    db.session.add(new_user)
    db.session.commit()

    send_confirmation_mail(new_user)

    return make_response("User created, not activated", 201)


@users_bp.route("/users/confirm/<string:public_id>", methods=["GET"], endpoint="confirm_mail")
def confirm_mail(public_id):
    # sql_activate_user(cursor, public_id)

    return make_response("User activated", 200)


@users_bp.route("/users", methods=["GET"], endpoint="get_all_users")
@token_required
def get_all_users(current_user):
    print(f"user = {current_user.username}")
    print("[Warning] Need to check if user is admin")
    db = current_app.db
    users = db.session.query(User).all()

    users_data = [{"id": user.public_id, "username": user.username, "email": user.mail} for user in users]

    return jsonify(users_data)


@users_bp.route("/users/<int:id>", methods=["GET"], endpoint="get_user_from_id")
@token_required
def get_user_from_id(current_user, id):
    print("[Warning] Need to check if user is admin")
    return f"One user: {id}"


@users_bp.route("/users/<string:username>", methods=["DELETE"], endpoint="remove_user_from_id")
# @token_required
# def remove_user_from_id(current_user, username):
def remove_user_from_id(username):
    print("[Warning] Need to check if user is admin or if the request if from same person")
    db = current_app.db
    user_to_delete = db.session.query(User).where(User.username == username).first()
    db.session.delete(user_to_delete)
    db.session.commit()

    return make_response("User deleted", 200)
