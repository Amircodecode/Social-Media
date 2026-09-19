import os
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 1025)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "mailhog"),
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=False,
    VALIDATE_CERTS=False,
)

fm = FastMail(conf)


async def send_verification_email(email: str, token) -> None:
    base_url = os.getenv("APP_BASE_URL", "http://localhost:8000")
    link = f"{base_url}/auth/verify?token={token}"

    message = MessageSchema(
        subject="Подтверди свою почту",
        recipients=[email],
        body=f"Привет!\n\nПерейди по ссылке, чтобы подтвердить почту:\n{link}\n\nСсылка действует 24 часа.",
        subtype=MessageType.plain,
    )
    await fm.send_message(message)
