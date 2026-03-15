from fastapi import APIRouter
from models import SessionDep, Brand, BrandModel
from sqlmodel import select
import httpx
from services.fipe_service import update_brands_if_needed, update_brand_models_if_needed
from schemas.vehicle import BrandRead, VehicleType

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

@catch_router.get("/{path_vehicle_type}/brands/", response_model=BrandRead) #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands
async def get_brands(path_vehicle_type: VehicleType, session: SessionDep):

    await update_brands_if_needed(session, path_vehicle_type)

    query = select(Brand).where(Brand.vehicle_type == path_vehicle_type)
    brands = session.exec(query).all()

    return brands

@catch_router.get("/{path_vehicle_type}/brands/{path_brand_code}/models/")
async def get_brand_models(path_vehicle_type, path_brand_code, session: SessionDep):

    await update_brand_models_if_needed(session, path_vehicle_type, path_brand_code)

    query = select(BrandModel).where(BrandModel.brand_code == path_vehicle_type, BrandModel.brand_code == path_brand_code)
    brand_models = session.exec(query).all()
    
    return brand_models

@catch_router.get("/vehicles") #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands/{brandId}/models
async def get_brand_vehicles(session: SessionDep):
    ...

@catch_router.get("/years") #
async def get_brand_vehicle_years(session: SessionDep):
    ...