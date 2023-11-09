from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete


db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    @classmethod
    def add(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def get_all(cls) -> list:
        instance = db.session.query(cls).all()
        return instance

    @classmethod
    def get_first_where(cls, statement):
        instance = db.session.query(cls).filter(statement).first()
        return instance

    @classmethod
    def delete_where(cls, statement):
        delete_query = delete(cls).where(statement)
        db.session.execute(delete_query)
        db.session.commit()

    @property
    def to_dict(self):
        values = self.__dict__
        values.pop("_sa_instance_state")
        return values

    def __repr__(self):
        repr_value = ""
        for key, value in self.to_dict.items():
            repr_value += f"{key} = {value}, "

        return repr_value
