import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI

from models import create_db_and_tables
from models import SessionDep
from models import (User,Vehicle)
from schemas.vehicle import CreateVehicle

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("Shutting down app")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/create", response_model=User)
def create_user(user: User, session: SessionDep) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/addVehicle", response_model=CreateVehicle)
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
