# own
import v1
from shared_models import db
from utils import get_mysql_uri

# pip
from flask import Flask
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()


app.config["SQLALCHEMY_DATABASE_URI"] = get_mysql_uri()


db.init_app(app)

with app.app_context():
    db.create_all()

app.db = db

for pages in v1.__all__:
    app.register_blueprint(getattr(v1, pages), url_prefix="/V1")

if __name__ == "__main__":
    app.run(debug=True)
