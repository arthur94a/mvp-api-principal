from datetime import datetime, timedelta
import httpx
from sqlmodel import select

from models.brand import Brand
from models.brand_model import BrandModel
from models.cache_control import CacheControl

FIPE_URL = "https://fipe.parallelum.com.br/api/v2/"
BRANDS_URL = FIPE_URL + "{param_vehicle_type}/brands/"
MODELS_URL = BRANDS_URL + "{param_brand_code}/models/"


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
        response = await client.get(BRANDS_URL.format(param_vehicle_type=input_vehicle_type))
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

""""
UPDATE BRANDS MODELS IF NEEDED
"""
async def update_brand_models_if_needed(session, input_vehicle_type, input_brand_code):
    query = select(BrandModel).where(BrandModel.vehicle_type == input_vehicle_type, BrandModel.brand_code == input_brand_code)
    models = session.exec(query).all()
    first = session.exec(query).first()

    if models:
        print("Tabéla de Modelos aqui")
        print(first)
        return

    else:
        async with httpx.AsyncClient() as client:
            response = await client.get(MODELS_URL.format(
                param_vehicle_type=input_vehicle_type, 
                param_brand_code=input_brand_code
            ))
            data = response.json()
        
        existing_codes = {
            code for code in session.exec(
                select(BrandModel.brand_code).where(Brand.brand_code == input_brand_code)
            )
        }
        
        new_brand_models = [
            BrandModel(
                model_code = item_model["code"],
                model_name = item_model["name"],
                brand_code = input_brand_code,
                vehicle_type = input_vehicle_type
            )
            for item_model in data
            if item_model["code"] not in existing_codes
        ]

        session.add_all(new_brand_models)
        print(data)
    
    session.commit()

    return