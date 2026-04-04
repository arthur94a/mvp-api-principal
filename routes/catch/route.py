
from typing import List
from fastapi import APIRouter, HTTPException
from models import SessionDep, Brand, BrandModel, BrandModelYear, Vehicle
from sqlmodel import select
from services.fipe_service import update_brands, update_brand_models, update_brand_model_years, update_vehicle
from schemas.vehicle import BrandRead, VehicleType

catch_router = APIRouter()

@catch_router.get("/{path_vehicle_type}/brands/", status_code=200, response_model=List[BrandRead]) #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands
async def get_brands(path_vehicle_type: VehicleType, session: SessionDep):

    await update_brands(session, path_vehicle_type)

    query = select(Brand).where(Brand.vehicle_type == path_vehicle_type)
    brands = session.exec(query).all()

    return brands

@catch_router.get("/{path_vehicle_type}/brands/{path_brand_code}/models/", status_code=200, response_model=List[BrandModel]) #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands/{brandId}/models/
async def get_brand_models(path_vehicle_type: VehicleType, path_brand_code: int, session: SessionDep):

    await update_brand_models(session, path_vehicle_type, path_brand_code)

    query = select(BrandModel).where(
        BrandModel.vehicle_type == path_vehicle_type,
        BrandModel.brand_code == path_brand_code
    )

    brand_models = session.exec(query).all()
    
    return brand_models

@catch_router.get("/{path_vehicle_type}/brands/{path_brand_code}/models/{path_model_code}", status_code=200, response_model=List[BrandModelYear]) #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands/{brandId}/models/{modelId}/years
async def get_brand_model_years(path_vehicle_type : VehicleType, path_brand_code: int, path_model_code: str, session: SessionDep):

    await update_brand_model_years(session, path_vehicle_type, path_brand_code, path_model_code)

    query = select(BrandModelYear).where(
        BrandModelYear.vehicle_type == path_vehicle_type,
        BrandModelYear.brand_code == path_brand_code,
        BrandModelYear.model_code == path_model_code
    )

    brand_model_years = session.exec(query).all()
    
    return brand_model_years

@catch_router.get("/{path_vehicle_type}/brands/{path_brand_code}/models/{path_model_code}/years/{path_year_code}", status_code=200) #https://fipe.parallelum.com.br/api/v2/{vehicleType}/brands/{brandId}/models/{modelId}/years/{yearId}
async def get_vehicle(
    path_vehicle_type : VehicleType,
    path_brand_code: int,
    path_model_code: str,
    path_year_code: str,
    session: SessionDep
):

    await update_vehicle(
        session,
        path_vehicle_type,
        path_brand_code,
        path_model_code,
        path_year_code
    )

    query = select(Vehicle).where(
        Vehicle.vehicle_type == path_vehicle_type,
        Vehicle.brand_code == path_brand_code,
        Vehicle.model_code == path_model_code,
        Vehicle.year_code == path_year_code
    )

    vehicle = session.exec(query).first()

    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    return vehicle