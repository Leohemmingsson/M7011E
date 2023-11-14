# own
import v1

# pip
from flask import Flask

app = Flask(__name__)


for pages in v1.__all__:
    app.register_blueprint(getattr(v1, pages), url_prefix="/V1")

if __name__ == "__main__":
    app.run(host="0.0.0.0")


# @app.route("/user")
# def user():
#     worker.send_task("user.create_user", kwargs={"name": "Bob"})
#     return "<p>Hello, World!</p>"


# @app.route("/item")
# def item():
#     worker.send_task("item.create_item", kwargs={"name": "Bowl"})
#     return "<p>Hello, World!</p>"


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True)
