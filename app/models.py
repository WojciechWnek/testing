from sqlmodel import Field, SQLModel


class WrestlerBase(SQLModel):
    name: str
    finisher: str
    catchphrase: str
    active: bool = True


class Wrestler(WrestlerBase, table=True):
    __tablename__: str = "wrestlers"

    id: int | None = Field(default=None, primary_key=True)


class WrestlerCreate(WrestlerBase):
    pass


class WrestlerUpdate(SQLModel):
    name: str | None = None
    finisher: str | None = None
    catchphrase: str | None = None
    active: bool | None = None


class UserBase(SQLModel):
    email: str


class User(SQLModel, table=True):
    __tablename__: str = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    hashed_password: str
    role: str = "user"


class UserCreate(UserBase):
    password: str
    role: str = "user"


class UserPublic(UserBase):
    id: int
    role: str
