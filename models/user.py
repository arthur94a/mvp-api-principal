from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from datetime import datetime
import zoneinfo

BRT = zoneinfo.ZoneInfo("America/Sao_Paulo")
def now_brt():
    return datetime.now(BRT)

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    password_hash: str
    create_at: datetime = Field(default_factory=now_brt)
    updated_at: datetime = Field(default_factory=now_brt)
