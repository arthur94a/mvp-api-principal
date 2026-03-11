from pydantic import BaseModel
from pydantic import EmailStr

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    password: str
