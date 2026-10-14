from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from src.config import get_session

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/token")


SessionDep = Annotated[Session, Depends(get_session)]
My_token = Annotated[str, Depends(oauth2_schema)]
