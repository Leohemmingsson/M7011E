# std
import datetime

# own
from permissions import check_password_hash
from task_worker import get_user_by_username

# pip
from flask import Blueprint, request, make_response, jsonify
import jwt

authentication_pb = Blueprint("authentication", __name__)

# NEED TO BE MOVED IN PRODUCTION
SECRET_KEY = "thisissecretkey"


@authentication_pb.route("/login", endpoint="login")
def login():
    """
    Path to login with basic auth, this returns a token that can be used to access the api.
    Default TTL for a token is 30 minutes.
    """
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    req = get_user_by_username.delay(auth.username)
    user, status_code = req.get()

    if status_code != 200:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    if user["activated"] is not True:
        return make_response("User not activated", 401)

    if check_password_hash(auth.password, user["password"]):
        token = jwt.encode(
            {"public_id": user["public_id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            SECRET_KEY,
        )

        return jsonify({"token": token})

    return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})
