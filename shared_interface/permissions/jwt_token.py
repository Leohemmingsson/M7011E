# std
from functools import wraps
import os

# own
from task_worker import get_user_by_public_id

# pip
from flask import request, jsonify, make_response
import jwt


def token_required(func):
    @wraps(func)
    def decoratorated(*args, **kwargs):
        if "x-access-token" not in request.headers:
            return jsonify({"message": "Token is missing"}, 401)

        token = request.headers["x-access-token"]

        try:
            data = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            req = get_user_by_public_id.delay(data["public_id"])
            response, status_code = req.get()
            if status_code != 200:
                return make_response(response, status_code)
            current_user = response
        except Exception as e:
            print(f"[Warning] specify exception as {type(e)} in jwt_token.py")
            return make_response("Token is invalid", 401)

        return func(current_user, *args, **kwargs)

    return decoratorated
