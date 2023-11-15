# own
from shared_models import BaseModel, session

# pip
from sqlalchemy import Column, String, Enum, Boolean, ForeignKey, Integer, delete
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "User"

    public_id = Column(String(255), primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    password = Column(String(255))
    address_id = Column(Integer, ForeignKey("Address.id"))
    type = Column(Enum("CUSTOMER", "ADMIN", "SUPERUSER"))
    mail = Column(String(255))
    activated = Column(Boolean)

    # relationships
    address = relationship("Address", back_populates="users")
    user_verification = relationship("UserVerification", uselist=False, back_populates="user")

    @classmethod
    def add(cls, verification_info, *args, **kwargs):
        user = cls(*args, **kwargs)

        user.user_verification = verification_info

        session.add(user)
        session.add(verification_info)
        session.commit()
        return user

    @classmethod
    def delete_where(cls, statement):
        user = session.query(cls).filter(statement).first()
        verification_info = user.user_verification
        session.delete(verification_info)
        session.delete(user)
        session.commit()

