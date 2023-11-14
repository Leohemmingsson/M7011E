# std
import os

# pip
from sqlalchemy import delete, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("mysql://root:root@db:3306/main")

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()

# Declare a base class for declarative models
Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def add(cls, *args, **kwargs):
        instance = cls(*args, **kwargs)
        session.add(instance)
        session.commit()
        return instance

    @classmethod
    def get_all(cls) -> list:
        instance = session.query(cls).all()
        return instance

    @classmethod
    def get_first_where(cls, statement):
        instance = session.query(cls).filter(statement).first()
        return instance

    @classmethod
    def delete_where(cls, statement):
        delete_query = delete(cls).where(statement)
        session.execute(delete_query)
        session.commit()

    @property
    def to_dict(self):
        values = self.__dict__
        values.pop("_sa_instance_state")
        return values

    def update(self, key, value):
        setattr(self, key, value)
        session.commit()

    def __repr__(self):
        repr_value = ""
        for key, value in self.to_dict.items():
            repr_value += f"{key} = {value}, "

        return repr_value
