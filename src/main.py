from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer


from src.config import create_db, SECRET_KEY
from src.models import Role, User
from src.routers import role_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(user_router)
app.include_router(role_router)


@app.get("/")
def root():
    return {"messege": "Api is runing"}


print(SECRET_KEY)
