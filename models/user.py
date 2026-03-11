from pydantic import EmailStr
from sqlmodel import Field
from schemas.base import TimestampModel

class User(TimestampModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str
