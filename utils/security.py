from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    print("🔥 HASH SENDO CHAMADO")
    print("VALOR:", password)
    print("BYTES:", len(password.encode("utf-8")))

    if len(password.encode("utf-8")) > 72:
        raise ValueError("Senha muito grande")
    
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)