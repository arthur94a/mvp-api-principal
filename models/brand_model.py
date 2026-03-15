from schemas.base import TimestampModel
from sqlmodel import Field
from sqlalchemy import UniqueConstraint
from schemas.vehicle import VehicleType

class BrandModel(TimestampModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "model_code",
            "brand_code",
            "vehicle_type",
            name="unique_brand_model"
        ),
    )

    model_code: str = Field(primary_key=True)
    model_name: str
    brand_code: str = Field(foreign_key="brand.brand_code")
    vehicle_type: VehicleType