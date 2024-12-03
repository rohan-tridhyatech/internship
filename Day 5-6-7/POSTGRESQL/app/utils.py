from __future__ import annotations

from datetime import datetime
from datetime import timedelta

from fastapi_mail import ConnectionConfig
from fastapi_mail import FastMail
from fastapi_mail import MessageSchema
from fastapi_mail import MessageType
from jose import jwt  # For creating and verifying JWT tokens
from passlib.context import CryptContext
from pydantic import SecretStr  # To securely store secrets like the email password

# For password hashing and verification

# Email configuration for sending order confirmation emails
conf = ConnectionConfig(
    MAIL_USERNAME="rohanmovaliya64@gmail.com",  # Sender's email
    # Securely store the email password
    MAIL_PASSWORD=SecretStr("bwyd hbkk sdwn turs"),
    MAIL_FROM="rohanmovaliya64@gmail.com",  # Sender's email address
    MAIL_PORT=587,  # SMTP port for Gmail
    MAIL_SERVER="smtp.gmail.com",  # Gmail SMTP server
    MAIL_STARTTLS=True,  # Use TLS encryption
    MAIL_SSL_TLS=False,  # Do not use SSL
    USE_CREDENTIALS=True,  # Enable authentication for email
    VALIDATE_CERTS=True,  # Validate the certificates for the server
)

# Secret key and algorithm for JWT creation and expiration time
# Key for JWT encoding/decoding
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"  # Hashing algorithm for JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Default expiration time for access tokens

# Function to send order confirmation email asynchronously


async def send_order_confirmation(email: str, order_id: int):
    # HTML content for the confirmation email
    html = f"<p>Thanks for placing an order. Your Order ID is {order_id}.</p>"
    # Create a message schema for the email
    message = MessageSchema(
        subject="Order Confirmation",  # Email subject
        recipients=[email],  # List of recipients (email)
        body=html,  # Email body (HTML format)
        subtype=MessageType.html,  # Setting the email type to HTML
    )
    # Create a FastMail instance with the email configuration
    fm = FastMail(conf)
    await fm.send_message(message)  # Send the email
    # Log the email sending
    print(f"Order confirmation email sent to {email} for Order ID: {order_id}")


# Password hashing context using bcrypt algorithm
# Create a password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to hash a plain password


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)  # Return the hashed password


# Function to verify a password by comparing plain and hashed passwords


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Return True if the passwords match
    return pwd_context.verify(plain_password, hashed_password)


# Function to create an access token (JWT) with expiration time


def create_access_token(data: dict, expire_delta: timedelta | None):
    to_encode = data.copy()  # Make a copy of the data to encode
    if expire_delta:
        # Set expiration time using the given delta
        expire = datetime.now() + expire_delta
    else:
        # Default expiration time is 15 minutes
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})  # Add the expiration time to the payload
    # Encode the JWT using the secret key and algorithm
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt  # Return the encoded JWT
