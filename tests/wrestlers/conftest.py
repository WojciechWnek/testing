import pytest
from sqlmodel import Session

from app import models  # noqa: F401


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
