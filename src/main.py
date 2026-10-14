from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import SECRET_KEY, create_db
from src.models import Role, User
from src.routers import auth_router, role_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(user_router)
app.include_router(role_router)
app.include_router(auth_router)


def root():
    return {"messege": "Api is runing"}


print(SECRET_KEY)
