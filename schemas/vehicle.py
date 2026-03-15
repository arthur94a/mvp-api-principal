from pydantic import BaseModel
from enum import Enum

class VehicleType(str, Enum):
    car = 'cars'
    motorcycles = 'motorcycles'
    trucks = 'trucks'

class BrandRead(BaseModel):
    brand_code: str
    brand_name: str
    vehicle_type: VehicleType

class CreateVehicleSchema(BaseModel):
    fipe_code: str
    type: VehicleType
    year_code: str