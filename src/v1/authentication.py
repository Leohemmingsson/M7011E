# std
import os
import datetime

# own
from permissions import check_password_hash
from orm import User

# pip
from flask import Blueprint, request, make_response, jsonify, current_app
import jwt

authentication_pb = Blueprint("authentication", __name__)


@authentication_pb.route("/login", endpoint="login")
def login():
    """
    Path to login with basic auth, this returns a token that can be used to access the api.
    Default TTL for a token is 30 minutes.
    """
    db = current_app.db
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    user = db.session.query(User).where(User.username == auth.username).first()

    if not user:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    if check_password_hash(auth.password, user.password):
        token = jwt.encode(
            {"public_id": user.public_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            os.getenv("SECRET_KEY"),
        )

        return jsonify({"token": token})

    return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
