from sqlmodel import select
from fastapi import APIRouter
import httpx
from models import SessionDep
from models import Vehicle
from schemas.vehicle import CreateVehicleSchema
from schemas.base import need_update

vehicle_router = APIRouter()

@vehicle_router.get("/")
async def root():
    return {"message": "Hello from Vehicle route"}


@vehicle_router.post("/fipe/add", response_model=Vehicle)
def add_vehicle_by_fipe(create_vehicle: CreateVehicleSchema, session: SessionDep) -> Vehicle:
    vehicle_fipe_code = create_vehicle.fipe_code
    vehicle_type = create_vehicle.type.value
    vehicle_year_code = create_vehicle.year_code

    vehicle = session.get(Vehicle, (vehicle_fipe_code,vehicle_year_code))

    if (vehicle):
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
   
    if not vehicle:
        print("🧙‍♂️ Criando veículo 🚗")
        vehicle = Vehicle (
            id = data["codeFipe"],
            vehicle_type = vehicle_type,
            brand = data["brand"],
            model = data["model"],
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