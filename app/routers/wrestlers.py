from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import col, select

from app.database import SessionDep
from app.models import Wrestler, WrestlerCreate, WrestlerUpdate

router = APIRouter(prefix="/wrestlers", tags=["wrestlers"])


def get_wrestler_or_404(session: SessionDep, wrestler_id: int) -> Wrestler:
    wrestler = session.get(Wrestler, wrestler_id)
    if not wrestler:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wrestler {wrestler_id} not found",
        )
    return wrestler


WrestlerDep = Annotated[Wrestler, Depends(get_wrestler_or_404)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Wrestler])
def get_wrestlers(session: SessionDep):
    return session.exec(select(Wrestler)).all()


@router.get("/search", status_code=status.HTTP_200_OK, response_model=list[Wrestler])
def search_wrestlers(
    session: SessionDep,
    name: str | None = None,
    active: bool | None = None,
):
    statement = select(Wrestler)

    if name:
        statement = statement.where(col(Wrestler.name).ilike(f"%{name}%"))

    if active is not None:
        statement = statement.where(Wrestler.active == active)

    return session.exec(statement).all()


@router.get("/{wrestler_id}", status_code=status.HTTP_200_OK, response_model=Wrestler)
def get_wrestler(wrestler: WrestlerDep):
    return wrestler


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Wrestler)
def create_wrestler(session: SessionDep, wrestler_payload: WrestlerCreate):
    wrestler = Wrestler.model_validate(wrestler_payload)
    session.add(wrestler)
    session.commit()
    session.refresh(wrestler)
    return wrestler


@router.patch("/{wrestler_id}", status_code=status.HTTP_200_OK, response_model=Wrestler)
def update_wrestler(
    session: SessionDep, wrestler: WrestlerDep, wrestler_update: WrestlerUpdate
):
    fields_to_update = wrestler_update.model_dump(exclude_unset=True)
    wrestler.sqlmodel_update(fields_to_update)

    session.add(wrestler)
    session.commit()
    session.refresh(wrestler)

    return wrestler


@router.delete("/{wrestler_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wrestler(session: SessionDep, wrestler: WrestlerDep):
    session.delete(wrestler)
    session.commit()
