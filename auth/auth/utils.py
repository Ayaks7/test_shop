import jwt
from jwt import PyJWTError
from typing import Optional
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from auth.models import ProfileUser

# Задаем секретный ключ иалгоритм шифрования
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# Инициализируем криптографию
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password, hashed_password):
    """Сверяем пароль с хэшем."""
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(password: str, user_password: str):
    """Аутентифицируем пользователя."""
    if not verify_password(password, user_password):
        return False
    return True


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """Создание временного токена."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Получаем пользователя по токену."""
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    user = await ProfileUser.get_objects_by_id(int(user_id))
    if user is None:
        raise credentials_exception
    return user
