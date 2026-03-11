from sqlmodel import Field
from sqlalchemy import Column, Numeric
from decimal import Decimal
from schemas.base import TimestampModel
from schemas.vehicle import VehicleType

class Vehicle(TimestampModel, table=True):
    id: str = Field(primary_key=True) # FIPE code
    vehicle_type: VehicleType
    brand: str
    brand_code: str
    model: str
    model_code: str
    year: int
    year_code: str
    price: Decimal = Field(sa_column=Column(Numeric(10, 2)))
    fuel: bool
