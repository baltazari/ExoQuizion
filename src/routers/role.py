from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from src.config import SessionDep
from src.models import Role
from src.schemas import AddRole, CheckRole

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    responses={404: {"description": "page not found"}},
)


@router.post(
    "/",
    response_model=CheckRole,
    status_code=status.HTTP_201_CREATED,
)
def create_role(role_data: AddRole, session: SessionDep):
    # check Role
    statment = select(Role).where(Role.role == role_data.role)

    existing_role = session.exec(statment).first()

    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Role already Exist!",
        )

    new_role = Role(
        role=role_data.role,
    )
    session.add(new_role)
    session.commit()
    session.refresh(new_role)

    return new_role
