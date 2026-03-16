from schemas.base import TimestampModel
from sqlmodel import Field
from sqlalchemy import UniqueConstraint
from schemas.vehicle import VehicleType

class BrandModelYear(TimestampModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "year_code",
            "model_code",
            "brand_code",
            "vehicle_type",
            name="unique_brand_model_year"
        ),
    )

    year_code: str = Field(primary_key=True)
    year_name: str
    model_code: str = Field(foreign_key="brandmodel.model_code")
    brand_code: int = Field(foreign_key="brand.brand_code")
    vehicle_type: VehicleType
    