from flask import Flask
import os

# from flask_sqlalchemy import SQLAlchemy
from shared_models import db
from dotenv import load_dotenv

# from orm import db
import v1


app = Flask(__name__)

load_dotenv()

USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST")
PORT = os.getenv("DB_PORT")
DATABASE = os.getenv("DB_DATABASE")


app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"


db.init_app(app)

with app.app_context():
    db.create_all()

app.db = db

for pages in v1.__all__:
    app.register_blueprint(getattr(v1, pages), url_prefix="/V1")

if __name__ == "__main__":
    app.run(debug=True)
