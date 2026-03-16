from pydantic import BaseModel
from enum import Enum

class VehicleType(str, Enum):
    car = 'cars'
    motorcycles = 'motorcycles'
    trucks = 'trucks'

class BrandRead(BaseModel):
    brand_code: int
    brand_name: str
    vehicle_type: VehicleType

class CreateVehicleSchema(BaseModel):
    brand_code: int
    model_code: str
    year_code: str
    vehicle_type: VehicleType

class CreateVehicleByFipeSchema(BaseModel):
    fipe_code: str
    year_code: str
    vehicle_type: VehicleType