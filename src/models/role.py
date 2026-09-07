from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .users import User


class Role(SQLModel, table=True):
    id: int | None = Field(
        default=None,
        primary_key=True,
    )
    role: str = Field(
        unique=True,
        index=True,
        max_length=50,
    )
    users: list["User"] = Relationship(back_populates="role")
