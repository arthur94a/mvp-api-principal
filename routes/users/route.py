from fastapi import APIRouter
from models import SessionDep
from models import User
from schemas.user import CreateUser

user_router = APIRouter()

@user_router.get("/")
async def root():
    return {"message": "Hello from User route"}

@user_router.post("/create", response_model=User)
def create_user(user_input: CreateUser, session: SessionDep) -> User:
    db_user = User(
        name=user_input.name,
        email=user_input.email,
        password_hash=user_input.password # Aqui você linka os nomes diferentes
    )
    
    # 2. Adicionar ao banco
    session.add(db_user)
    session.commit()
    
    # 3. Atualizar o objeto com os dados do banco (como o ID gerado)
    session.refresh(db_user)
    
    return db_user

@user_router.post("/test")
def test_user(session: SessionDep):
    user = session.get(User, 2)

    if (user) :
        print(user)

        name = user.name
        print(name)
    
    else:
        print("Nao encontrado")
        user = None
    
    return user