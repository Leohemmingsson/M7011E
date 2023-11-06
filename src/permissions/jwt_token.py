# std
from functools import wraps
import os

# own
from connections import SqlManager, sql_get_user_from_pid

# pip
from flask import request, jsonify
import jwt


def token_required(func):
    @wraps(func)
    def decoratorated(*args, **kwargs):
        if "x-access-token" not in request.headers:
            return jsonify({"message": "Token is missing"}, 401)

        token = request.headers["x-access-token"]

        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            with SqlManager() as (cursor, mydb):
                current_user = sql_get_user_from_pid(cursor, data["public_id"])
        except Exception as e:
            print(f"[Warning] specify exception as {type(e)} in jwt_token.py")
            return jsonify({"message": "Token is invalid"}, 401)

        return func(current_user, *args, **kwargs)

    return decoratorated
