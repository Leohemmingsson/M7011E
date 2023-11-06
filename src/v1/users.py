# std
import uuid

# own
from permissions import token_required, hash_password
from data_types import User

# pip
from flask import Blueprint, make_response, request

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["POST"], endpoint="create_user")
@token_required
def create_user(current_user):
    print("[Warning] Need to check if user is admin, otherwise anyone can create a user, or maybe mail check?")

    data = request.get_json()

    hashed_password = hash_password(data["password"])
    new_user = User(public_id=str(uuid.uuid4()), username=data["name"], password=hashed_password, type="user")

    print(new_user)

    return make_response("User created", 201)


@users_bp.route("/users", methods=["GET"], endpoint="get_all_users")
@token_required
def get_all_users(current_user):
    print("[Warning] Need to check if user is admin, otherwise anyone can create a user, or maybe mail check?")
    return "Users"


@users_bp.route("/users/<int:id>", methods=["GET"], endpoint="get_useruser__from_id")
@token_required
def get_user_from_id(current_user, id):
    print("[Warning] Need to check if user is admin, otherwise anyone can create a user, or maybe mail check?")
    return f"One user: {id}"
