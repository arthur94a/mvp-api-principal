from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy import UniqueConstraint
from schemas.base import TimestampModel
from schemas.vehicle import VehicleType

class Brand(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "code",
            "type",
            name="unique_brand"
        ),
    )

    code: str = Field(primary_key=True)
    name: str
    type: VehicleType
    