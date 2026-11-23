from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import select

from app.database import SessionDep
from app.dependencies.auth import UserDep
from app.models import User, UserCreate, UserPublic

router = APIRouter(tags=["users"])


def require_admin(user: UserDep) -> User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserPublic
)
def register(session: SessionDep, user_data: UserCreate):
    fake_hash_password = user_data.password + "abc"

    user = User(
        email=user_data.email, hashed_password=fake_hash_password, role=user_data.role
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/token", status_code=status.HTTP_200_OK)
def login(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = session.exec(select(User).where(User.email == form_data.username)).first()
    fake_hash_password = form_data.password + "abc"

    if not user or user.hashed_password != fake_hash_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return {"access_token": user.email, "token_type": "bearer"}


@router.get("/users/me", status_code=status.HTTP_200_OK, response_model=UserPublic)
def get_me(user: UserDep):
    return user


@router.get(
    "/admin/users",
    status_code=status.HTTP_200_OK,
    response_model=list[UserPublic],
    dependencies=[Depends(require_admin)],
)
def get_all_users(session: SessionDep):
    return session.exec(select(User)).all()
