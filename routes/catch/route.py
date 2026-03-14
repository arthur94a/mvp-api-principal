from fastapi import APIRouter
from models import SessionDep, Brand
from sqlmodel import select
import httpx
from services.fipe_service import update_brands_if_needed

catch_router = APIRouter()

@catch_router.get("/")
async def root():

    response = httpx.get(
        f"https://fipe.parallelum.com.br/api/v2/cars/brands"
    )

    print(response)

    data = response.json()

    print(data)

    return {"message": "Hello from Catch route"}

@catch_router.get("/fipe")
async def get_fipe_code(session: SessionDep):
    ...

@catch_router.get("/brands/{vehicle_type}") #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands
async def get_brands(vehicle_type: str, session: SessionDep):

    await update_brands_if_needed(session, vehicle_type)

    brands = session.exec(
        select(Brand).where(Brand.type == vehicle_type)
    ).all()

    return brands

@catch_router.get("/vehicles") #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands/{brandId}/models
async def get_brand_vehicles(session: SessionDep):
    ...

@catch_router.get("/years") #
async def get_brand_vehicle_years(session: SessionDep):
    ...