from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Annotated

Password = Annotated[str, StringConstraints(min_length=6, max_length=72)]

class CreateUserSchema(BaseModel):
    name: str
    email: EmailStr
    password: Password

class UpdatePasswordSchema(BaseModel):
    user_id: int
    current_password: Password
    new_password: Password

class UserVehicleSchema(BaseModel):
    user_id: int
    vehicle_id: str
    year_code: str