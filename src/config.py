import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg://ghost:M1sh1k019891710@localhost:5432/exo"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)


def create_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
