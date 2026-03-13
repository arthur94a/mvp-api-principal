from sqlmodel import Field
from schemas.base import TimestampModel
class UserVehicle(TimestampModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    vehicle_id: str = Field(foreign_key="vehicle.id", primary_key=True)