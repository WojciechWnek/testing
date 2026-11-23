import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app import models  # noqa: F401
from app.database import get_session
from main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def wrestler(session: Session):
    undertaker = models.Wrestler(
        name="The Undertaker",
        finisher="Tombstone Piledriver",
        catchphrase="Rest in peace",
        active=True,
    )
    session.add(undertaker)
    session.commit()
    session.refresh(undertaker)
    return undertaker


@pytest.fixture
def inactive_wrestler(session: Session):
    rock = models.Wrestler(
        name="The Rock",
        finisher="Rock Bottom",
        catchphrase="Can you smell what the Rock is cooking?",
        active=False,
    )
    session.add(rock)
    session.commit()
    session.refresh(rock)
    return rock


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
