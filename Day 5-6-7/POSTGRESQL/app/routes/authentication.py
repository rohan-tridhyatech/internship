from __future__ import annotations

from datetime import timedelta

from app import utils
from app.auth import get_current_user
from app.auth import get_user_by_username
from app.database import get_session
from app.models import Users
from app.utils import create_access_token
from app.utils import get_password_hash
from app.utils import verify_password
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

# FastAPI imports
# Importing database session and authentication utilities

router = APIRouter()

# Register a new user (POST /register)


@router.post("/register", response_model=Users)
async def register_user(user: Users, session: Session = Depends(get_session)):
    # Check if the username already exists in the database
    existing_user = get_user_by_username(session, user.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists",
        )

    # Hash the user's password before saving it
    hashed_password = get_password_hash(user.password)

    # Create a new user instance
    new_user = Users(username=user.username, password=hashed_password, role=user.role)

    # Add the new user to the session and commit to the database
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Return a success message with the new user's details (excluding password)
    return {
        "message": "User registered successfully",
        "user": {"username": new_user.username, "role": new_user.role},
    }


# Login user and return a JWT token (POST /token)


@router.post("/token")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    # Fetch the user from the database using the provided username
    user = get_user_by_username(session, form_data.username)

    # If user does not exist or password is incorrect, raise an error
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Set token expiration time (e.g., 15 minutes)
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Create access token with user details and expiration time
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expire_delta=access_token_expires,
    )

    # Return the access token to the user
    return {"access_token": access_token, "token_type": "bearer"}


# Secure endpoint to read a conversation (GET /conversation)


@router.get("/conversation")
async def read_conversation(current_user: Users = Depends(get_current_user)):
    # Return a message indicating it's a secure conversation, with the user's details
    return {
        "conversation": "This is a secure conversation",
        "current_user": current_user.username,
        "role": current_user.role,
    }
