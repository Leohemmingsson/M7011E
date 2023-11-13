# std
import os
import datetime
import random

# own
from permissions import check_password_hash
from orm import User
from mail import send_verification_code

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

    if not user.activated:
        return make_response("Email is not verified", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})

    if check_password_hash(auth.password, user.password):
        verification_code = str(random.randint(100000, 999999))
        timestamp = datetime.datetime.utcnow()
        attempts = 3

        user.verification_code = verification_code
        user.verification_timestamp = timestamp
        user.verification_attempts = attempts

        db.session.commit()

        send_verification_code(user, verification_code)

        return make_response("Login verification code sent to your email.", 200)

    return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Login required!"'})


@authentication_pb.route("/verify", endpoint="verify", methods=["POST"])
def verify():
    """
    Path to verify the login with the verification code.
    """
    db = current_app.db
    auth = request.authorization

    verification_code = request.json.get("code")

    if not auth or not auth.username or not auth.password or not verification_code:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Verification required!"'})

    user = db.session.query(User).filter_by(username=auth.username).first()

    if not user or not user.verification_code:
        return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Verification required!"'})

    if user.verfication_attempts > 0:
        if verification_code == user.verification_code:
            expiration_time = user.verification_timestamp + datetime.timedelta(minutes=5)
            if datetime.datetime.utcnow() <= expiration_time:
                user.verification_code = None
                user.verification_timestamp = None
                user.verfication_attempts = None

                db.session.commit()

                token = jwt.encode(
                    {"public_id": user.public_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                    os.getenv("SECRET_KEY"),
                )

                return jsonify({"token": token})
        user.verfication_attempts -= 1
        db.session.commit()

    return make_response("Could not verify", 401, {"WWW-Authenticate": 'Basic realm="Verification required!"'})
