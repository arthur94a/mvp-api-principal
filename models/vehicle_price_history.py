from schemas.base import TimestampModel
from sqlalchemy import UniqueConstraint
from datetime import date
from sqlmodel import Field

class VehiclePriceHistory(TimestampModel, Table=True):
    __table_args__ = (
        UniqueConstraint(
            "vehicle_id",
            "reference_month",
            name="unique_vehicle_month"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    vehicle_id: str = Field(foreign_key=True)
    reference_month: date
    price: str


