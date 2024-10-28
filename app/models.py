# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    can_add_courses = Column(Integer, default=0)  # 0 - False, 1 - True
    can_view_users = Column(Integer, default=0)
    can_edit_courses = Column(Integer, default=0)
    can_view_progress = Column(Integer, default=0)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    date_birth = Column(String, nullable=True)  # Можно изменить на Date
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'))  # Связь с таблицей ролей

    role = relationship("Role")  # Отношение с моделью Role

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey('users.id'))  # Создатель курса
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_create = Column(String, nullable=False)  # Можно изменить на Date

    creator = relationship("User")  # Связь с пользователем (создателем курса)

class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey('courses.id'))  # Связь с курсом
    type_id = Column(Integer, ForeignKey('type_module.id'))  # Связь с типом модуля
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    order_number = Column(Integer, nullable=False)

class TypeModule(Base):
    __tablename__ = "type_module"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Theory(Base):
    __tablename__ = "theory"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey('modules.id'))  # Связь с модулем
    content = Column(String, nullable=False)

class Test(Base):
    __tablename__ = "tests"

    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(Integer, ForeignKey('modules.id'))  # Связь с модулем
    total_points = Column(Integer, nullable=False)

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(Integer, ForeignKey('tests.id'))  # Связь с тестом
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

class VariantAnswer(Base):
    __tablename__ = "variant_answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey('questions.id'))  # Связь с вопросом
    name = Column(String, nullable=False)
    is_true = Column(Integer, default=0)  # 0 - False, 1 - True

class AnswerUser(Base):
    __tablename__ = "answer_user"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Связь с пользователем
    variant_answer_id = Column(Integer, ForeignKey('variant_answers.id'))  # Связь с вариантом ответа
    date = Column(String, nullable=False)  # Можно изменить на Date