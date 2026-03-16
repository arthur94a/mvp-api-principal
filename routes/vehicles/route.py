from sqlmodel import select
from fastapi import APIRouter
import httpx
from models import SessionDep, Brand, BrandModel
from models.vehicle import Vehicle
from schemas.vehicle import CreateVehicleSchema, CreateVehicleByFipeSchema
from schemas.base import need_update

vehicle_router = APIRouter()

@vehicle_router.post("/add", response_model=Vehicle)
def add_vehicle(
    create_vehicle: CreateVehicleSchema,
    session: SessionDep
) -> Vehicle:
    
    vehicle_brand_code = create_vehicle.brand_code
    vehicle_model_code = create_vehicle.model_code
    vehicle_year_code = create_vehicle.year_code
    vehicle_type = create_vehicle.vehicle_type.value

    query = select(Vehicle).where(
        Vehicle.brand_code == vehicle_brand_code,
        Vehicle.model_code == vehicle_model_code,
        Vehicle.year_code == vehicle_year_code
    )

    vehicle = session.exec(query).first()

    if vehicle:
        print("🧙‍♂️ Buscando veículo... 🔎")
        current_date = vehicle.updated_at

        if not need_update(current_date):
            print("🧙‍♂️ Este veículo já está na sua garagem ✔️")
            return vehicle
        
        print("🧙‍♂️ Atualizando veículo... ♻️")

    response = httpx.get(
        f"https://fipe.parallelum.com.br/api/v2/{vehicle_type}/brands/{vehicle_brand_code}/models/{vehicle_model_code}/years/{vehicle_year_code}"
    )

    data = response.json()

    query_by_fipe = select(Vehicle).where(Vehicle.id == data["codeFipe"])
    vehicle_by_fipe = session.exec(query_by_fipe).first()

    if not vehicle and not vehicle_by_fipe:
        print("🧙‍♂️ Criando veículo 🚗")
        vehicle = Vehicle (
            id = data["codeFipe"],
            vehicle_type = vehicle_type,
            brand = data["brand"],
            brand_code = vehicle_brand_code,
            model = data["model"],
            model_code = vehicle_model_code,
            year = data["modelYear"],
            year_code = vehicle_year_code,
            price = data["price"],
            fuel = data["fuel"]
        )

        session.add(vehicle)
    
    if not vehicle:
        print("🧙‍♂️ Atualizando dados e valor do veículo 🚗")
        def update_if_none(obj, field, value):
            if getattr(obj, field) is None:
                setattr(obj, field, value)

        vehicle_by_fipe.price = data["price"]
        update_if_none(vehicle_by_fipe, "brand_code", vehicle_brand_code)
        update_if_none(vehicle_by_fipe, "model_code", vehicle_model_code)
        update_if_none(vehicle_by_fipe, "year_code", vehicle_year_code)

    else:
        print("🧙‍♂️ Atualizando valor do veículo 🚗")
        vehicle.price = data["price"]

    vehicle_to_return = vehicle or vehicle_by_fipe
    session.commit()
    session.refresh(vehicle_to_return)

    print("🧙‍♂️ Pronto, veículo na garagem ✔️")

    return vehicle_to_return


@vehicle_router.post("/fipe/add", response_model=Vehicle)
def add_vehicle_by_fipe(
    create_vehicle: CreateVehicleByFipeSchema,
    session: SessionDep
) -> Vehicle:
    
    vehicle_fipe_code = create_vehicle.fipe_code
    vehicle_type = create_vehicle.vehicle_type.value
    vehicle_year_code = create_vehicle.year_code

    vehicle = session.get(Vehicle, (vehicle_fipe_code,vehicle_year_code))

    if vehicle:
        print("🧙‍♂️ Buscando veículo... 🔎")
        current_date = vehicle.updated_at

        if not need_update(current_date):
            print("🧙‍♂️ Este veículo já está na sua garagem ✔️")
            return vehicle
        
        print("🧙‍♂️ Atualizando veículo... ♻️")

    response = httpx.get(
        f"https://fipe.parallelum.com.br/api/v2/{vehicle_type}/{vehicle_fipe_code}/years/{vehicle_year_code}"
    )

    data = response.json()

    brand_name = data["brand"]
    model_name = data["model"]

    # cruzar marca
    brand = session.exec(
        select(Brand).where(Brand.brand_name == brand_name)
    ).first()

    print(brand)

    brand_code = brand.brand_code if brand else None

    # cruzar modelo
    model = session.exec(
        select(BrandModel).where(
            BrandModel.model_name == model_name
        )
    ).first()

    model_code = model.model_code if model else None
   
    if not vehicle:
        print("🧙‍♂️ Criando veículo 🚗")
        vehicle = Vehicle (
            id = data["codeFipe"],
            vehicle_type = vehicle_type,
            brand=brand_name,
            brand_code=brand_code,
            model=model_name,
            model_code=model_code,
            year = data["modelYear"],
            year_code = vehicle_year_code,
            price = data["price"],
            fuel = data["fuel"]
        )

        session.add(vehicle)

    else:
        print("🧙‍♂️ Atualizando valor do veículo 🚗")
        vehicle.price = data["valor"]

    session.commit()
    session.refresh(vehicle)

    print("🧙‍♂️ Pronto, veículo na garagem ✔️")

    return vehicle