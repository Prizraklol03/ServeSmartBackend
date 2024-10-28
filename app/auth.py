# app/auth.py
from fastapi import APIRouter, HTTPException, Depends, Response
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt  # PyJWT для создания токенов
from . import database, models, schemas
from .hashing import hash_password, verify_password
from .dependencies import get_db

router = APIRouter()

# Конфигурация для JWT токенов
SECRET_KEY = "prizraklol03"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Время жизни access_token
REFRESH_TOKEN_EXPIRE_DAYS = 7  # Время жизни refresh_token

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db), response: Response = None):
    try:
        if user.password != user.confirm_pass:
            response.status_code = 400  # Устанавливаем статус 400 Bad Request
            return {"detail": "Passwords do not match"}

        # Хэширование пароля и добавление в базу данных
        hashed_password = hash_password(user.password)
        new_user = models.User(
            name=user.name,
            surname=user.surname,
            email=user.email,
            hashed_password=hashed_password,
            patronymic=user.patronymic,
            date_birth=user.date_birth,
            phone_number=user.phone_number,
            role_id=user.role_id
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        response.status_code = 201  # Устанавливаем статус 201 Created
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.post("/login")
async def login(user_data: schemas.UserLogin, db: Session = Depends(get_db), response: Response = None):
    user = db.query(models.User).filter(models.User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        response.status_code = 401  # Устанавливаем статус 401 Unauthorized
        return {"detail": "Invalid credentials"}

    # Создание данных для токена
    token_data = {"sub": user.email, "user_id": user.id}

    # Генерация токенов
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)

    response.status_code = 200  # Устанавливаем статус 200 OK
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/password-reset")
async def password_reset(password_reset_request: schemas.PasswordResetRequest, db: Session = Depends(get_db), response: Response = None):
    user = db.query(models.User).filter(models.User.email == password_reset_request.email).first()
    if not user:
        response.status_code = 404  # Устанавливаем статус 404 Not Found
        return {"detail": "Email not found"}

    # Здесь вы можете реализовать логику отправки email для сброса пароля
    # Например, отправить email с временной ссылкой для сброса пароля

    response.status_code = 200  # Устанавливаем статус 200 OK
    return {"detail": "Password reset link sent to your email"}
