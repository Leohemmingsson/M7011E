from flask import Flask
from flask_sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from orm import BaseModel
import v1

app = Flask(__name__)

engine = create_engine("sqlite:///database.db")
Session = sessionmaker(bind=engine)
session = Session()

BaseModel.metadata.create_all(engine)

for pages in v1.__all__:
    app.register_blueprint(getattr(v1, pages), url_prefix="/V1")


if __name__ == "__main__":
    app.run()
