import pytest
from sqlmodel import Session

from app import models  # noqa: F401


@pytest.fixture
def user(session: Session):
    boris = models.User(email="boris@example.com", hashed_password="secret123abc")
    session.add(boris)
    session.commit()
    session.refresh(boris)
    return boris


@pytest.fixture
def admin(session: Session):
    vince = models.User(
        email="admin@example.com", hashed_password="secret123abc", role="admin"
    )
    session.add(vince)
    session.commit()
    session.refresh(vince)
    return vince
