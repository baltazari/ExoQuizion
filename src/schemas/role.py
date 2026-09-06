from pydantic import BaseModel, Field


class AddRole(BaseModel):
    role: str = Field(max_length=50)


class CheckRole(BaseModel):
    id: int
    role: str
