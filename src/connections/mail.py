# std
import os

# own
from orm import User

# pip
from flask_mail import Message, current_app
from flask import request


def send_confirmation_mail(user: User) -> Message:
    """
    Create confirmation mail.
    """
    print(f"{request.url = }")
    mail = current_app.mail
    msg = Message(subject="Confirm mail", sender=os.getenv("MAIL_USERNAME"), recipients=[user.mail])
    msg.body = f"Hello {user.username}\nConfirm mail: http://localhost:5000/users/confirm/{user.public_id}"

    mail.send(msg)
