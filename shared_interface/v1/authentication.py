# std
import datetime

# own
from permissions import check_password_hash
from task_worker import (
    get_user_by_username,
    create_user_verification,
    get_user_verification_by_public_id,
    set_user_verification_attempts_zero,
)
from mail import send_verification_code

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

    if not check_password_hash(auth.password, user["password"]):
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    req = create_user_verification.delay(user["public_id"])
    user_verification_code, status_code = req.get()

    send_verification_code(user, user_verification_code)

    return make_response("Login verification code sent to your email.", 200)


@authentication_pb.route("/verify", endpoint="verify", methods=["POST"])
def verify():
    """
    Path to verify the login with the verification code.
    """

    username = request.json.get("username")
    verification_code = request.json.get("code")

    if not username or not verification_code:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Verification required!"'})

    req = get_user_by_username.delay(username)
    user, status_code = req.get()

    if not user:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Verification required!"'})

    req = get_user_verification_by_public_id.delay(user["public_id"])
    user_verification_info, status_code = req.get()

    if status_code != 200:
        return make_response("Could not verify", 401)

    if verification_code != user_verification_info["code"]:
        return make_response("Could not verify", 401)

    expiration_time = user_verification_info["timestamp"] + datetime.timedelta(minutes=5)
    if datetime.datetime.utcnow() > expiration_time:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Verification required!"'})

    req = set_user_verification_attempts_zero.delay(user["public_id"])

    token = jwt.encode(
        {"public_id": user["public_id"], "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        SECRET_KEY,
    )

    return jsonify({"token": token})
