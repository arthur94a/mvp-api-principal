
from typing import List
from fastapi import APIRouter
from models import SessionDep, Brand, BrandModel, BrandModelYear
from sqlmodel import select
from services.fipe_service import update_brands, update_brand_models, update_brand_model_years
from schemas.vehicle import BrandRead, VehicleType

catch_router = APIRouter()

@catch_router.get("/{path_vehicle_type}/brands/", response_model=List[BrandRead]) #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands
async def get_brands(path_vehicle_type: VehicleType, session: SessionDep):

    await update_brands(session, path_vehicle_type)

    query = select(Brand).where(Brand.vehicle_type == path_vehicle_type)
    brands = session.exec(query).all()

    return brands

@catch_router.get("/{path_vehicle_type}/brands/{path_brand_code}/models/") #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands/{brandId}/models/
async def get_brand_models(path_vehicle_type: VehicleType, path_brand_code: int, session: SessionDep):

    await update_brand_models(session, path_vehicle_type, path_brand_code)

    query = select(BrandModel).where(
        BrandModel.vehicle_type == path_vehicle_type,
        BrandModel.brand_code == path_brand_code
    )

    brand_models = session.exec(query).all()
    
    return brand_models

@catch_router.get("/{path_vehicle_type}/brands/{path_brand_code}/models/{path_model_code}") #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands/{brandId}/models/{modelId}/years
async def get_brand_model_years(path_vehicle_type : VehicleType, path_brand_code: int, path_model_code: str, session: SessionDep):

    await update_brand_model_years(session, path_vehicle_type, path_brand_code, path_model_code)

    query = select(BrandModelYear).where(
        BrandModelYear.vehicle_type == path_vehicle_type,
        BrandModelYear.brand_code == path_brand_code,
        BrandModelYear.model_code == path_model_code
    )

    brand_model_years = session.exec(query).all()
    
    return brand_model_years