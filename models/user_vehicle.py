from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from datetime import datetime
import zoneinfo

BRT = zoneinfo.ZoneInfo("America/Sao_Paulo")
def now_brt():
    return datetime.now(BRT)

class UserVehicle(SQLModel, table=True):
    ser_id: int = Field(foreign_key="user.id", primary_key=True)
    vehicle_id: str = Field(foreign_key="vehicle.id", primary_key=True)
    create_at: datetime = Field(default_factory=now_brt)