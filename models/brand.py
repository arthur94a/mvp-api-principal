from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint
from schemas.vehicle import VehicleType

class Brand(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "brand_code",
            "vehicle_type",
            name="unique_brand"
        ),
    )

    brand_code: int = Field(primary_key=True)
    brand_name: str
    vehicle_type: VehicleType
    