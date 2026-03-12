from typing import Optional
from sqlmodel import Field
from schemas.base import TimestampModel
from schemas.vehicle import VehicleType

class Vehicle(TimestampModel, table=True):
    id: str = Field(primary_key=True) # FIPE code
    year_code: str = Field(primary_key=True)
    year: int
    vehicle_type: VehicleType
    brand: str
    brand_code: str | None = Field(default=None)
    model: str
    model_code: Optional[str] = Field(default=None)
    price: str
    fuel: Optional[str] = Field(default=None)
