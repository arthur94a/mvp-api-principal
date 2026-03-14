from typing import Optional
from typing import List, TYPE_CHECKING
from sqlmodel import Field, Relationship
from schemas.base import TimestampModel
from schemas.vehicle import VehicleType
from .user_vehicle import UserVehicle

if TYPE_CHECKING:
    from .user import User

class Vehicle(TimestampModel, table=True):
    id: str = Field(primary_key=True) # FIPE code
    year_code: str = Field(primary_key=True)
    year: int
    vehicle_type: VehicleType
    brand: str
    brand_code: str = Field(foreign_key="brand.code")
    model: str
    model_code: str = Field(foreign_key="brandmodel.code")
    price: str
    fuel: Optional[str] = Field(default=None)

    users: List["User"] = Relationship(
        back_populates="vehicles",
        link_model=UserVehicle
    )
