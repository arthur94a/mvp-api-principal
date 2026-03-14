from pydantic import BaseModel
from pydantic import EmailStr

class CreateUserSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
