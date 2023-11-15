# pip
from sqlalchemy import create_engine
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
    def get_first_where(cls, statement, staement2=None):
        if staement2 is None:
            instance = session.query(cls).filter(statement).first()
        else:
            instance = session.query(cls).filter(statement, staement2).first()

        return instance

    @classmethod
    def get_all_where(cls, statement, statement2=None) -> list:
        if statement2 is None:
            instance = session.query(cls).filter(statement).all()
        else:
            instance = session.query(cls).filter(statement, statement2).all()

        return instance

    @classmethod
    def delete_where(cls, statement, statement2=None) -> None:
        if statement2 is None:
            session.query(cls).filter(statement).delete()
        else:
            session.query(cls).filter(statement, statement2).delete()

    @property
    def to_dict(self) -> dict:
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
