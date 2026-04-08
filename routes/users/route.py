from fastapi import APIRouter, HTTPException
from sqlmodel import select
from utils.security import hash_password
from models import SessionDep
from models.user import User
from models.vehicle import Vehicle
from schemas.user import CreateUserSchema, UserVehicleSchema, UpdatePasswordSchema, PublicUserSchema, UserLoginSchema, ResponseUserLoginSchema
from models import UserVehicle
from utils.security import verify_password, hash_password
from typing import List

user_router = APIRouter()

@user_router.get("/")
async def root():
    return {"message": "Hello from User route"}


@user_router.post("/create", status_code=201, response_model=PublicUserSchema)
def create_user(user_input: CreateUserSchema, session: SessionDep) -> User:
    print("🧙‍♂️ Criando um novo user.")

    user = User(
        name=user_input.name,
        email=user_input.email,
        password_hash=hash_password(user_input.password)  # 🔐 HASH AQUI
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    print("🧙‍♂️ Usuário adicionado!")

    return user

@user_router.post("/login", status_code=200, response_model=ResponseUserLoginSchema)
def login_user(user_input: UserLoginSchema, session: SessionDep):
    email = user_input.email
    password = user_input.password

    query = select(User).where(User.email == email)
    session_user = session.exec(query).first()

    if not session_user or not verify_password(password, session_user.password_hash):
        raise HTTPException(
            status_code=400, 
            detail={
                "message": "Email ou senha inválidos",
                "status":"fail"
            }
        )
    
    return {
        "message": "Login realizado com sucesso",
        "status":"success",
        "data": {
            "id": session_user.id,
            "email": session_user.email,
            "name": session_user.name
        }
    }


# 🔐 Atualizar senha
@user_router.put("/password/update", status_code=204)
def update_password(data: UpdatePasswordSchema, session: SessionDep):

    user = session.get(User, data.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 🔐 Verifica hash corretamente
    if not verify_password(data.current_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")

    # 🔐 Nova senha com hash
    user.password_hash = hash_password(data.new_password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return


# 💀 Deletar usuário
@user_router.delete("/delete/{user_id}", status_code=204)
def delete_user(user_id: int, session: SessionDep):

    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 🔥 Remove vínculos com veículos
    statement = select(UserVehicle).where(UserVehicle.user_id == user_id)
    user_vehicles = session.exec(statement).all()

    for uv in user_vehicles:
        session.delete(uv)

    # ❌ Remove usuário
    session.delete(user)
    session.commit()

    print("💀 Conta deletada.")
    return

@user_router.post("/vehicle/add", status_code=201, response_model=UserVehicle)
def add_vehicle(user_vehicle: UserVehicleSchema, session: SessionDep):

    print("🧙‍♂️ Adicionando veículo na sua garagem... 🚗")

    # Verifica se já existe (evita duplicidade na PK composta)
    has_user_vehicle = session.get(
        UserVehicle,
        (user_vehicle.user_id, user_vehicle.vehicle_id, user_vehicle.year_code)
    )

    if has_user_vehicle:
        print("🚗 Veículo já esta na sua garagem.")
        raise HTTPException(status_code=409, detail="Veículo já existe")
    
    search_vehicle = session.get(Vehicle, (user_vehicle.vehicle_id, user_vehicle.year_code))

    if not search_vehicle:
        print("🚗 Veículo não encontrado.")
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    # Cria o vínculo
    new_vehicle = UserVehicle(
        user_id=user_vehicle.user_id,
        vehicle_id=user_vehicle.vehicle_id,
        year_code=user_vehicle.year_code
    )

    session.add(new_vehicle)
    session.commit()
    session.refresh(new_vehicle)

    print("🚗 Veículo adicionado à garagem.")

    return new_vehicle

@user_router.delete("/vehicle/remove", status_code=204)
def remove_vehicle(user_vehicle: UserVehicleSchema , session: SessionDep):
    vehicle = session.get(UserVehicle, (user_vehicle.user_id, user_vehicle.vehicle_id, user_vehicle.year_code))

    if not vehicle:
        return

    session.delete(vehicle)
    session.commit()

    print("🧙‍♂️ Seu carro foi removido da garagem pessoal.")

    return

@user_router.get("/vehicle", status_code=200)
def get_user_vehicle(
    user_id: int,
    vehicle_id: str,
    year_code: str,
    session: SessionDep
) -> UserVehicle:
    vehicle = session.get(UserVehicle, (user_id, vehicle_id, year_code))

    print("🧙‍♂️ Buscando veículo na garagem pessoal... 🔍")
    print(vehicle)

    if not vehicle:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    return vehicle

@user_router.get("/vehicles", status_code=200, response_model=List[Vehicle])
def list_user_vehicles(user_id: int, session: SessionDep):

    user = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # 🔥 pega os veículos através do relacionamento
    vehicles = [uv.vehicle for uv in user.vehicles]

    return vehicles