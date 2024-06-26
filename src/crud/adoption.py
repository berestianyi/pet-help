from src.models import Questionnaire
from src import db


def add_questionnaire(pet_id, personal_info_id):
    new_questionnaire = Questionnaire(pet_id=pet_id, personal_info_id=personal_info_id)
    db.session.add(new_questionnaire)
    db.session.commit()
    return new_questionnaire | None
