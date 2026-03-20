from datetime import datetime, timedelta
import httpx
from sqlmodel import select
from models import Brand, BrandModel, BrandModelYear
from models.cache_control import CacheControl

FIPE_URL = "https://fipe.parallelum.com.br/api/v2/"
BRANDS_URL = FIPE_URL + "{param_vehicle_type}/brands/"
MODELS_URL = BRANDS_URL + "{param_brand_code}/models/"
YEARS_URL = MODELS_URL + "{param_model_code}/years/"


""""
UPDATE BRANDS IF NEEDED
This function update the brands each (int) days
"""
async def update_brands(session, input_vehicle_type):
    DAYS_TO_UPDATE = 10

    cache = session.get(CacheControl, ("brands", input_vehicle_type))

    if cache and datetime.utcnow() - cache.updated_at < timedelta(days=DAYS_TO_UPDATE):
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(BRANDS_URL.format(param_vehicle_type=input_vehicle_type.value))
        data = response.json()

    existing_codes = {
        code for code in session.exec(
            select(Brand.brand_code).where(Brand.vehicle_type == input_vehicle_type)
        )
    }

    new_brands = [
        Brand(brand_code=int(b["code"]), brand_name=b["name"], vehicle_type=input_vehicle_type)
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
UPDATE BRAND MODELS IF NEEDED
Each brand has own models.
They are updated in DB by brand
"""
async def update_brand_models(session, input_vehicle_type, input_brand_code):
    query = select(BrandModel).where(
        BrandModel.vehicle_type == input_vehicle_type,
        BrandModel.brand_code == input_brand_code
    )

    models = session.exec(query).all()

    # se existir e ainda não passou 10 dias
    if models:
        first = models[0]
        if datetime.utcnow() - first.updated_at < timedelta(days=10):
            print("🧙‍♂️ Tabela atualizada recentemente.")
            return
    
    # se não existir ou estiver desatualizado
    async with httpx.AsyncClient() as client:
        print("🧙‍♂️ Ooh, Solicitando modelos dados da API 🐣")
        response = await client.get(
            MODELS_URL.format(
                param_vehicle_type=input_vehicle_type.value,
                param_brand_code=input_brand_code
            )
        )

    data = response.json()

    print("🧙‍♂️ Validando os dados existentes")
    existing_codes = {
        code for code in session.exec(
            select(BrandModel.model_code).where(
                BrandModel.brand_code == input_brand_code
            )
        )
    }

    new_models = [
        BrandModel(
            model_code=item["code"],
            model_name=item["name"],
            brand_code=int(input_brand_code),
            vehicle_type=input_vehicle_type,
            updated_at=datetime.utcnow()
        )
        for item in data
        if item["code"] not in existing_codes
    ]

    session.add_all(new_models)
    session.commit()

    return

""""
UPDATE BRAND MODEL YEARS IF NEEDED
Each brand has own models.
Each model has own years.
They are updated in DB by brand
"""
async def update_brand_model_years(
    session,
    input_vehicle_type,
    input_brand_code,
    input_model_code
):
    query = select(BrandModelYear).where(
        BrandModelYear.vehicle_type == input_vehicle_type,
        BrandModelYear.brand_code == input_brand_code,
        BrandModelYear.model_code == input_model_code
    )

    years = session.exec(query).all()

    # se existir e ainda não passou 10 dias
    if years:
        first = years[0]
        if datetime.utcnow() - first.updated_at < timedelta(days=10):
            print("🧙‍♂️ Tabela atualizada recentemente.")
            return

    # se não existir ou estiver desatualizado
    async with httpx.AsyncClient() as client:
        print("🧙‍♂️ Ooh, Solicitando anos dados da API 🐣")
        response = await client.get(
            YEARS_URL.format(
                param_vehicle_type=input_vehicle_type.value,
                param_brand_code=input_brand_code,
                param_model_code=input_model_code
            )
        )

    data = response.json()

    print("🧙‍♂️ Validando os dados existentes")
    existing_codes = {
        code for code in session.exec(
            select(BrandModelYear.year_code).where(
                BrandModelYear.brand_code == input_brand_code,
                BrandModelYear.model_code == input_model_code
            )
        )
    }

    new_years = [
        BrandModelYear(
            year_code=item['code'],
            year_name=item['name'],
            model_code=input_model_code,
            brand_code=int(input_brand_code),
            vehicle_type=input_vehicle_type,
            updated_at=datetime.utcnow()
        )
        for item in data
        if item["code"] not in existing_codes
    ]

    session.add_all(new_years)
    session.commit()

    return