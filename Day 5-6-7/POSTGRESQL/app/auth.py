from __future__ import annotations

from app import utils
from app.database import get_session
from app.models import Users
from app.schemas import TokenData
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlmodel import select
from sqlmodel import Session

# Importing necessary utilities and models

# OAuth2 password bearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to retrieve user by username from the database


def get_user_by_username(session: Session, username: str):
    return session.exec(select(Users).where(Users.username == username)).first()


# Dependency to get the current user based on JWT token


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> Users:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't Validate Credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])

        # Extract the username from the payload
        username: str | None = payload.get("sub")

        if username is None:
            raise credentials_exception  # Raise exception if no username is found

        # Create a token_data object with the username
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception  # Raise exception if the token is invalid or expired

    # Fetch the user from the database using the username
    user = get_user_by_username(session, username=token_data.username)

    if user is None:
        raise credentials_exception  # Raise exception if user does not exist

    return user


# Function to get the current user's role from the JWT token


def get_current_user_role(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the JWT token to extract the payload
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])

        # Extract the role from the payload
        role = payload.get("role")

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Role information missing in token",
            )
        return role
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


# Dependency to check if the current user has admin role


def admin_only(role: str = Depends(get_current_user_role)):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted",  # Raise an exception if the role is not admin
        )
    return role
