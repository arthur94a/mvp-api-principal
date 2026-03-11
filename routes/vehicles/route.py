from fastapi import APIRouter
import httpx
from models import SessionDep
from schemas.vehicle import CreateVehicle

vehicle_router = APIRouter()

@vehicle_router.get("/")
async def root():
    return {"message": "Hello from Vehicle route"}


@vehicle_router.post("/addVehicle", response_model=CreateVehicle)
def add_vehicle(create_vehicle: CreateVehicle, session: SessionDep) -> CreateVehicle:
    vehicle_fipe = create_vehicle.fipe_code
    vehicle_type = create_vehicle.vehicle_type.value
    print(create_vehicle)

    response = httpx.get(
        f"https://fipe.parallelum.com.br/api/v2/{vehicle_type}/{vehicle_fipe}/years"
    )

    data = response.json()

    print(data)

    # vehicle = Vehicle(
    #     id=data["codigoFipe"],
    #     brand=data["marca"],
    #     model=data["modelo"]
    # )

    # session.add(vehicle)
    # session.commit()
    # session.refresh(vehicle)

    return create_vehicle