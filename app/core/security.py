from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

class SecurityManager:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def hash_password(password: str) -> str:
        return SecurityManager.pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return SecurityManager.pwd_context.verify(plain_password, hashed_password)

class JWTManager:
    SECRET_KEY = "your_secret_key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=JWTManager.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWTManager.SECRET_KEY, algorithm=JWTManager.ALGORITHM)
        return encoded_jwt
