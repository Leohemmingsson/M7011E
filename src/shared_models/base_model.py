from flask_sqlalchemy import SQLAlchemy  # Should import Model, cant find it


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def add(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance
