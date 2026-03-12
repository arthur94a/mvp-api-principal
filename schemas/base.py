from datetime import datetime
import zoneinfo
from sqlmodel import SQLModel, Field

BRT = zoneinfo.ZoneInfo("America/Sao_Paulo")

def now_brt():
    return datetime.now(BRT)

def need_update(updated_at: datetime) -> bool:
    now = now_brt()

    return (
        updated_at.year != now.year or
        updated_at.month != now.month
    )

class TimestampModel(SQLModel):
    created_at: datetime = Field(default_factory=now_brt)
    updated_at: datetime = Field(
        default_factory=now_brt, 
        sa_column_kwargs={"onupdate": now_brt} # Atualiza automaticamente no banco
    )