from schemas.base import TimestampModel
from sqlmodel import Field
from sqlalchemy import UniqueConstraint
from schemas.vehicle import VehicleType
from typing import Optional

class BrandModelYear(TimestampModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    year_code: str
    year_name: str
    model_code: str = Field(foreign_key="brandmodel.model_code")
    brand_code: int = Field(foreign_key="brandmodel.brand_code")
    vehicle_type: VehicleType

    __table_args__ = (
        UniqueConstraint(
            "year_code",
            "model_code",
            "brand_code",
            "vehicle_type",
            name="unique_brand_model_year"
        ),
    )
    