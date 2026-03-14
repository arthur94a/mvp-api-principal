from datetime import datetime, timedelta
import httpx
from sqlmodel import select

from models.brand import Brand
from models.cache_control import CacheControl

FIPE_URL = "https://fipe.parallelum.com.br/api/v2/{param_vehicle_type}/brands"


""""
UPDATE BRANDS IF NEEDED
This function update the brands each (int) days
"""
async def update_brands_if_needed(session, input_vehicle_type):
    DAYS_TO_UPDATE = 10

    cache = session.get(CacheControl, ("brands", input_vehicle_type))

    if cache and datetime.utcnow() - cache.updated_at < timedelta(days=DAYS_TO_UPDATE):
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(FIPE_URL.format(param_vehicle_type=input_vehicle_type))
        data = response.json()

    existing_codes = {
        code for code in session.exec(
            select(Brand.brand_code).where(Brand.vehicle_type == input_vehicle_type)
        )
    }

    new_brands = [
        Brand(brand_code=b["code"], brand_name=b["name"], vehicle_type=input_vehicle_type)
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
                vehicle_type=input_vehicle_type
            )
        )

    session.commit()