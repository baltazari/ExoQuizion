import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class CreateUser(BaseModel):
    username: str = Field(min_length=4, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    role_id: int


class CheckUser(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    updated_at: datetime
