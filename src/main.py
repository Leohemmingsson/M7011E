# std
import os

# own
import v1
from shared_models import db

# pip
from flask import Flask
from flask_mail import Mail


app = Flask(__name__)

app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
app.config["MAIL_PORT"] = os.getenv("MAIL_PORT")
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = True if os.getenv("MAIL_USE_TLS") == "True" else False
app.config["MAIL_USE_SSL"] = True if os.getenv("MAIL_USE_TLS") == "True" else False
app.config["MAIL_DEBUG"] = True
mail = Mail(app)


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"


db.init_app(app)

with app.app_context():
    db.create_all()

app.db = db

for pages in v1.__all__:
    app.register_blueprint(getattr(v1, pages), url_prefix="/V1")

if __name__ == "__main__":
    app.run(debug=True)
