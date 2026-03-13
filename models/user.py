from pydantic import EmailStr
from typing import List
from sqlmodel import Field, Relationship
from schemas.base import TimestampModel
from models import UserVehicle, Vehicle

class User(TimestampModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str

    vehicles: List["Vehicle"] = Relationship(
        back_populates="users",
        link_model=UserVehicle
    )
