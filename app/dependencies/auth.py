from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import select

from app.database import SessionDep
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    email = token
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return user


UserDep = Annotated[User, Depends(get_current_user)]
