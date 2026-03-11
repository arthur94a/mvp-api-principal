from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Numeric
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from decimal import Decimal
import zoneinfo

BRT = zoneinfo.ZoneInfo("America/Sao_Paulo")
def now_brt():
    return datetime.now(BRT)

class VehicleType(str, Enum):
    car = 'cars'
    motorcyles = 'motorcyles'
    trucks = 'trucks'

class CreateVehicle(BaseModel):
    fipe_code: str
    vehicle_type: VehicleType

class Vehicle(SQLModel, table=True):
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
    create_at: datetime = Field(default_factory=now_brt)
    updated_at: datetime = Field(default_factory=now_brt)
