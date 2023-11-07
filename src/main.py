from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
from shared_models import db

# from orm import db
import v1


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
