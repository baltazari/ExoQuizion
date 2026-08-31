from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from config import create_db
from models.users import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/users/")
async def get_item(token: Annotated[str, Depends(oauth2_schema)]):
    return {"token": token}
