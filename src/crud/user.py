from src.models import PersonalInfo, User
from src import db


def get_user_by_username(username: str) -> User | None:
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    return user


def get_user_by_email(email: str) -> User | None:
    user = User.query.filter_by(email=email).first()
    if not user:
        return None
    return user


def get_personal_info(user) -> PersonalInfo | None:
    if user.is_authenticated:
        personal_info = PersonalInfo.query.filter_by(id=user.personal_info_id).first()
        return personal_info
    return None


def add_personal_info(user, full_name, phone, description, birth_date) -> PersonalInfo | None:
    personal_info = PersonalInfo(
        full_name=full_name, phone=phone, description=description, birth_date=birth_date
    )
    db.session.add(personal_info)
    db.session.commit()
    if user.is_authenticated:
        user.personal_info_id = personal_info.id
        db.session.commit()

    return personal_info


def get_personal_info_fields(personal_info) -> tuple:
    full_name = personal_info.full_name
    phone = personal_info.phone
    description = personal_info.description
    birth_date = personal_info.birth_date.strftime('%m/%d/%Y')
    return full_name, phone, description, birth_date


def add_user(username, email, password) -> User | None:
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def update_personal_info(user, full_name, phone, description, birth_date) -> PersonalInfo | None:
    personal_info = get_personal_info(user)
    if personal_info:
        personal_info.full_name = full_name
        personal_info.phone = phone
        personal_info.description = description
        personal_info.birth_date = birth_date
        db.session.commit()
        return personal_info
    return None

