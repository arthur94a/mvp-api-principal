from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
import os

# >>> MODELS HERE (START)
from .user import User
from .user_vehicle import UserVehicle
from .vehicle import Vehicle
from .vehicle_price_history import VehiclePriceHistory
from .brand import Brand
from .brand_model import BrandModel
from .cache_control import CacheControl
# <<< MODELS HERE (END)

# >>> CREATE DATABASE DIRECTORY (START)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PARENT_DIR = os.path.dirname(BASE_DIR)

DB_PATH = os.path.join(PARENT_DIR, "database")

if not os.path.exists(DB_PATH):
   os.makedirs(DB_PATH)
# <<< CREATE DATABASE DIRECTORY (END)

DB_URL = f"sqlite:///{DB_PATH}/database.db"

connect_args = {"check_same_thread": False}
engine = create_engine(DB_URL, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]