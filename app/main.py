# app/main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import database, models, schemas
from passlib.context import CryptContext
from app.hashing import hash_password  # импортируй hash_password из модуля hashing
from .auth import router as auth_router  # Импортируем роутер из auth
from .dependencies import get_db  # Импортируйте get_db из dependencies
from fastapi.middleware.cors import CORSMiddleware

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить все источники (можете указать конкретные, если нужно)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

app.include_router(auth_router)

# Создание таблиц
models.Base.metadata.create_all(bind=database.engine)

@app.get("/start")
def read_start_page(db: Session = Depends(get_db)):  # Используй get_db здесь
    return {"message": "Welcome!"}

@app.post("/users/")
def create_user(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(user_data.password)
        user = models.User(
            name=user_data.name,
            surname=user_data.surname,
            email=user_data.email,
            hashed_password=hashed_password,
            username=user_data.username  # Не забудь добавить username
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))