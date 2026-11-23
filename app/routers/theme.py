from typing import Annotated, Literal

from fastapi import APIRouter, Cookie, Response, status
from pydantic import BaseModel

router = APIRouter(tags=["theme"])

Theme = Literal["light", "dark"]


class ThemeRequest(BaseModel):
    value: Theme


@router.post("/theme", status_code=status.HTTP_201_CREATED)
def set_theme(theme_request: ThemeRequest, response: Response):
    response.set_cookie(key="theme", value=theme_request.value)
    return {"message": f"Theme set to {theme_request.value}"}


@router.get("/theme", status_code=status.HTTP_200_OK)
def get_theme(theme: Annotated[Theme, Cookie()] = "light"):
    return {"theme": theme}
