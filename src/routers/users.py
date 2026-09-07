from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from src.utils.security import hash_pass

from src.config import SessionDep
from src.models.users import User
from src.schemas.user import CheckUser, CreateUser

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post(
    "/",
    response_model=CheckUser,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: CreateUser,
    session: SessionDep,
):
    statment = select(User).where(
        (User.email == user_data.email) | (User.username == user_data.username)
    )
    existing_user = session.exec(statment).first()

    # Check Email
    if existing_user is not None and existing_user.email == user_data.email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registred",
        )
    # Check Username
    if existing_user is not None and existing_user.username == user_data.username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already taken",
        )

    # Create user
    user = User(
        email=user_data.email,
        username=user_data.username,
        password=hash_pass(user_data.password),
        role_id=user_data.role_id,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
