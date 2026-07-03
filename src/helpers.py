from models import User, Todo
from datetime import datetime

def parse_birth_date(date: str):
    return datetime.strptime(date, "%Y-%m-%d").date()


def user_from_json(user: dict) -> User:
    return User(
        id=user["id"],
        first_name=user["firstName"],
        last_name=user["lastName"],
        maiden_name=user["maidenName"],
        age=user["age"],
        gender=user["gender"],
        email=user["email"],
        phone=user["phone"],
        username=user["username"],
        password=user["password"],
        birth_date=parse_birth_date(user["birthDate"]),
        image=user["image"],
        blood_group=user["bloodGroup"],
        height=user["height"],
        weight=user["weight"],
        eye_color=user["eyeColor"],
        hair=user["hair"],
        ip=user["ip"],
        address=user["address"],
        country=user["address"]["country"],
        mac_address=user["macAddress"],
        university=user["university"],
        bank=user["bank"],
        company=user["company"],
        ein=user["ein"],
        ssn=user["ssn"],
        user_agent=user["userAgent"],
        crypto=user["crypto"],
        role=user["role"],
    )

def todo_from_json(todo:dict) -> Todo:
    return Todo(
        id=todo["id"],
        todo=todo["todo"],
        completed=todo["completed"],
        user_id=todo["userId"]
    )