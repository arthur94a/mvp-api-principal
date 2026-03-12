from fastapi import FastAPI
from contextlib import asynccontextmanager
from routes.users.route import user_router
from routes.vehicles.route import vehicle_router

from models import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    print("Shutting down app")

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(vehicle_router, prefix="/vehicles", tags=["Vehicles"])
