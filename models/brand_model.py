from sqlmodel import Field, Relationship
from sqlalchemy import UniqueConstraint
from schemas.base import TimestampModel

class BrandModel(TimestampModel, table=True):
    __table_args__ = (
        UniqueConstraint(
            "code",
            "name",
            name="unique_brand_model"
        ),
    )

    code: str = Field(primary_key=True)
    name: str