import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "ChangeThisToAStrongSecretKey123")

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "database", "helpdesk.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = UPLOAD_FOLDER

    # Mail Configuration
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True

    MAIL_USERNAME = os.environ.get(
        "MAIL_USERNAME",
        "sunilballewad@gmail.com"
    )

    MAIL_PASSWORD = os.environ.get(
        "MAIL_PASSWORD",
        "your_email_password"
    )

    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        "sunilballewad@gmail.com"
    )