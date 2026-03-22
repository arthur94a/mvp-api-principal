from pydantic import EmailStr
from typing import List, TYPE_CHECKING
from sqlmodel import Field, Relationship
from schemas.base import TimestampModel
from .user_vehicle import UserVehicle

if TYPE_CHECKING:
    from .vehicle import Vehicle

class User(TimestampModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(index=True, unique=True)
    password_hash: str

    vehicles: List["Vehicle"] = Relationship(
        back_populates="users",
        link_model=UserVehicle
    )
