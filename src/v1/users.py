from flask import Blueprint

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", endpoint="users")
def users():
    return "Users"


@users_bp.route("/users/<int:id>", endpoint="get_from_id")
def show():
    return f"One user: {id}"
