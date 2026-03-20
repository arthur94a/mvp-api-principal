from sqlmodel import Field
from sqlalchemy import ForeignKeyConstraint
from schemas.base import TimestampModel

class UserVehicle(TimestampModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    vehicle_id: str = Field(primary_key=True)
    year_code: str = Field(primary_key=True)

    __table_args__ = (
        ForeignKeyConstraint(
            ["vehicle_id", "year_code"],
            ["vehicle.id", "vehicle.year_code"]
        ),
    )