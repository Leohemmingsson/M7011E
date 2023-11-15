# own
import v1

# pip
from flask import Flask

app = Flask(__name__)


for pages in v1.__all__:
    app.register_blueprint(getattr(v1, pages), url_prefix="/V1")

if __name__ == "__main__":
    app.run(host="0.0.0.0")
