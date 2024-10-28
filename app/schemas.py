# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Схема для ролей
class RoleBase(BaseModel):
    name: str
    can_add_courses: Optional[bool] = False
    can_view_users: Optional[bool] = False
    can_edit_courses: Optional[bool] = False
    can_view_progress: Optional[bool] = False

# Схема для пользователей
class UserBase(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str] = None
    date_birth: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str
    confirm_pass: str
    role_id: Optional[int]  # Указываем роль при создании пользователя

class UserOut(UserBase):
    id: int
    hashed_password: str
    role_id: Optional[int]  # Включаем role_id в ответ

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

# Схемы для курсов и модулей
class CourseCreate(BaseModel):
    name: str
    description: str
    creator_id: int  # ID создателя курса

class ModuleCreate(BaseModel):
    course_id: int
    type_id: int  # ID типа модуля
    name: str
    description: Optional[str] = None
    order_number: int  # Порядковый номер модуля

# Схемы для теории и тестов
class TheoryCreate(BaseModel):
    module_id: int
    content: str

class TestCreate(BaseModel):
    module_id: int
    total_points: int

# Схемы для вопросов и вариантов ответов
class QuestionCreate(BaseModel):
    test_id: int
    name: str
    price: int

class VariantAnswerCreate(BaseModel):
    question_id: int
    name: str
    is_true: bool

# Схема для ответов пользователей
class AnswerUserCreate(BaseModel):
    user_id: int
    variant_answer_id: int