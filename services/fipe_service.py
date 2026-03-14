from datetime import datetime, timedelta
import httpx
from sqlmodel import select

from models.brand import Brand
from models.cache_control import CacheControl

FIPE_URL = "https://fipe.parallelum.com.br/api/v2/{vehicle_type}/brands"


async def update_brands_if_needed(session, vehicle_type):


    cache = session.get(CacheControl, ("brands", vehicle_type))

    if cache and datetime.utcnow() - cache.updated_at < timedelta(days=10):
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(FIPE_URL.format(vehicle_type=vehicle_type))
        data = response.json()

    existing_codes = {
        code for code in session.exec(
            select(Brand.code).where(Brand.type == vehicle_type)
        )
    }

    new_brands = [
        Brand(code=b["code"], name=b["name"], type=vehicle_type)
        for b in data
        if b["code"] not in existing_codes
    ]

    session.add_all(new_brands)

    if cache:
        cache.updated_at = datetime.utcnow()
    else:
        session.add(
            CacheControl(
                endpoint="brands",
                vehicle_type=vehicle_type
            )
        )

    session.commit()