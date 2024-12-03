from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Verilmiş şifrəni hash formatında qaytarır."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Hash formatındakı şifrəni təsdiqləyir."""
    return pwd_context.verify(plain_password, hashed_password)
