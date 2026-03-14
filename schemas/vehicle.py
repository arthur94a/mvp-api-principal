from pydantic import BaseModel
from enum import Enum

class VehicleType(str, Enum):
    car = 'cars'
    motorcycles = 'motorcycles'
    trucks = 'trucks'

class AddBrandSchema(BaseModel):
    code: str
    name: str
    type: VehicleType

class CreateVehicleSchema(BaseModel):
    fipe_code: str
    type: VehicleType
    year_code: str