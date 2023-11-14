# importing the Yagmail library
import os
import yagmail
from orm import User


def send_confirmation_email(user: User) -> None:
    USER = os.getenv("MAIL_USERNAME")
    PASSWORD = os.getenv("MAIL_PASSWORD")

    yag = yagmail.SMTP(user=USER, password=PASSWORD)

    yag.send(
        to=user.mail,
        subject="Confirm email",
        contents=f"Hello {user.username}!"
        f"\nPlease confirm your email by clicking on the link: http://localhost:5000/V1/users/confirm/{user.public_id}",
    )
