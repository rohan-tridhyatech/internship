from __future__ import annotations

from pydantic import BaseModel

# Import BaseModel from Pydantic for defining data models

# Token model to represent the structure of the access token response


class Token(BaseModel):
    access_token: str  # The JWT access token string
    token_type: str  # Type of token (usually "bearer")


# TokenData model to represent the structure of the token's decoded data (stored in the JWT)


class TokenData(BaseModel):
    username: str  # The username of the user extracted from the token
