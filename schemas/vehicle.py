from pydantic import BaseModel
from enum import Enum

class VehicleType(str, Enum):
    car = 'cars'
    motorcyles = 'motorcyles'
    trucks = 'trucks'

class CreateVehicleSchema(BaseModel):
    fipe_code: str
    type: VehicleType
    year_code: str