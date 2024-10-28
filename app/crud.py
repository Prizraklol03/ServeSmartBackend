# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Пользователи
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        hashed_password=hashed_password,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Роли
def create_role(db: Session, role: schemas.RoleBase):
    db_role = models.Role(
        name=role.name,
        can_add_courses=role.can_add_courses,
        can_view_users=role.can_view_users,
        can_edit_courses=role.can_edit_courses,
        can_view_progress=role.can_view_progress
    )
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

# Курсы
def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        name=course.name,
        description=course.description,
        date_create=course.date_create,
        creator_id=course.creator_id
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Модули
def create_module(db: Session, module: schemas.ModuleCreate):
    db_module = models.Module(
        course_id=module.course_id,
        type_id=module.type_id,
        name=module.name,
        description=module.description,
        order_number=module.order_number
    )
    db.add(db_module)
    db.commit()
    db.refresh(db_module)
    return db_module

# Теория
def create_theory(db: Session, theory: schemas.TheoryCreate):
    db_theory = models.Theory(
        module_id=theory.module_id,
        content=theory.content
    )
    db.add(db_theory)
    db.commit()
    db.refresh(db_theory)
    return db_theory

# Тесты
def create_test(db: Session, test: schemas.TestCreate):
    db_test = models.Test(
        module_id=test.module_id,
        total_points=test.total_points
    )
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

# Вопросы
def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(
        test_id=question.test_id,
        name=question.name,
        price=question.price
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Варианты ответов
def create_variant_answer(db: Session, variant_answer: schemas.VariantAnswerCreate):
    db_variant_answer = models.VariantAnswer(
        question_id=variant_answer.question_id,
        name=variant_answer.name,
        is_true=variant_answer.is_true
    )
    db.add(db_variant_answer)
    db.commit()
    db.refresh(db_variant_answer)
    return db_variant_answer

# Ответы пользователей
def create_answer_user(db: Session, answer_user: schemas.AnswerUserCreate):
    db_answer_user = models.AnswerUser(
        user_id=answer_user.user_id,
        variant_answer_id=answer_user.variant_answer_id
    )
    db.add(db_answer_user)
    db.commit()
    db.refresh(db_answer_user)
    return db_answer_user

# Другие функции для получения данных, обновления и удаления также можно добавить