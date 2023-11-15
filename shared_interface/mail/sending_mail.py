# importing the Yagmail library
import os
import yagmail
from dotenv import load_dotenv


def send_confirmation_email(user: dict) -> None:
    load_dotenv()
    USER = os.getenv("MAIL_USERNAME")
    PASSWORD = os.getenv("MAIL_PASSWORD")

    yag = yagmail.SMTP(user=USER, password=PASSWORD)

    yag.send(
        to=user["mail"],
        subject="Confirm email",
        contents=f"Hello {user['username']}!\nPlease confirm your email by clicking on the link: "
        f"http://localhost:8000/V1/users/confirm/{user['public_id']}",
    )


def send_verification_code(user: dict, code: str) -> None:
    load_dotenv()
    USER = os.getenv("MAIL_USERNAME")
    PASSWORD = os.getenv("MAIL_PASSWORD")

    yag = yagmail.SMTP(user=USER, password=PASSWORD)

    yag.send(
        to=user["mail"],
        subject="Verification code",
        contents=f"Hello {user['username']}!" f"\nPlease enter the following code {code}",
    )
