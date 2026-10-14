from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from sqlmodel import select

from src.config import (
    ALGORITHM,
    SECRET_KEY,
)
from src.models import User
from src.schemas.auth import TokenData
from src.utils.dependencies import My_token, SessionDep

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")


def hash_pass(password: str) -> str:
    return password_hash.hash(password)


def verify_pass(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)


def get_user(session: SessionDep, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    return session.exec(statement).first()


def authenticate_user(session: SessionDep, username: str, password: str):
    user = get_user(session, username)
    if user is None:
        verify_pass(password, DUMMY_HASH)
        return False
    if not verify_pass(password, user.password):
        return False
    return user


# Create jwt
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


async def get_curent_user(session: SessionDep, token: My_token):
    creadentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise creadentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise creadentials_exception
    user = get_user(session, username=token_data.username)
    if user is None:
        raise creadentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_curent_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
