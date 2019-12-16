from datetime import timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from auth import app
from auth.models import ProfileUser
from auth.utils import (
    authenticate_user,
    create_access_token,
)

# Время жизни токена
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@app.get("/auth/echo")
async def echo():
    return {'msg': 'Success'}


@app.post("/auth/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Первый логин, сверяем пароль с хэшем, выдаем временный токен."""

    # Ищем пользователя в базе по уникальному логину и сверяем пароли
    user_auth = None
    user = await ProfileUser.get_object_for_auth(form_data.username)
    if user:
        user_auth = authenticate_user(form_data.password, user.password)
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Пользователя не существует",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Генерируем и выдаем токен
    if not user_auth:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {'access_token': access_token}


@app.get("/auth/user/{user_id}")
async def get_user(
    user_id: int
):
    """Получение пользователя по идентификатору."""
    current_user = await ProfileUser.get_objects_by_id(user_id)
    if current_user:
        return {
            'ID': current_user.id,
            'Логин': current_user.username,
            'Емаил': current_user.email,
            'Адрес': current_user.address,
            'ФИО': current_user.full_name,
        }
    return 'Пользователь не найден'
