# std
from functools import wraps
import os

# own
# from orm import User

# pip
from flask import request, jsonify, current_app
import jwt


def token_required(func):
    @wraps(func)
    def decoratorated(*args, **kwargs):
        if "x-access-token" not in request.headers:
            return jsonify({"message": "Token is missing"}, 401)

        token = request.headers["x-access-token"]

        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            print(data)
            db = current_app.db
            current_user = db.session.query(User).where(User.public_id == data["public_id"]).first()
        except Exception as e:
            print(f"[Warning] specify exception as {type(e)} in jwt_token.py")
            return jsonify({"message": "Token is invalid"}, 401)

        return func(current_user, *args, **kwargs)

    return decoratorated
