from datetime import datetime
from sqlmodel import SQLModel, Field
from schemas.vehicle import VehicleType

class CacheControl(SQLModel, table=True):
    endpoint: str = Field(primary_key=True)
    vehicle_type: VehicleType = Field(primary_key=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)