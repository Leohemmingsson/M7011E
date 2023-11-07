# std
import os

# own
from data_types import User

# pip
from flask_mail import Message, current_app


def send_confirmation_mail(user: User) -> Message:
    """
    Create confirmation mail.
    """
    mail = current_app.extensions.get("mail")
    msg = Message(subject="Confirm mail", sender=os.getenv("MAIL_USERNAME"), recipients=[user.mail])
    msg.body = f"Hello {user.username}\nConfirm mail: http://localhost:5000/users/confirm/{user.public_id}"
    mail.send(msg)
