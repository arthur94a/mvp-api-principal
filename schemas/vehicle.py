from pydantic import BaseModel
from enum import Enum

class VehicleType(str, Enum):
    car = 'cars'
    motorcyles = 'motorcyles'
    trucks = 'trucks'

class CreateVehicle(BaseModel):
    fipe_code: str
    vehicle_type: VehicleType