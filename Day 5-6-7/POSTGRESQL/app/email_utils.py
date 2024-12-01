from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr, SecretStr

conf = ConnectionConfig(
    MAIL_USERNAME="rohanmovaliya64@gmail.com",
    MAIL_PASSWORD= SecretStr("bwyd hbkk sdwn turs"),
    MAIL_FROM="rohanmovaliya64@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


class EmailSchema(BaseModel):
    email: list[EmailStr]

async def send_order_confirmation(email: str, order_id: int):
    html = f"<p>Thanks for placing an order. Your Order ID is {order_id}.</p>"
    message = MessageSchema(
        subject="Order Confirmation",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    print(f"Order confirmation email sent to {email} for Order ID: {order_id}")
