from src.models import Questionnaire, Pet
from src import db


def add_questionnaire(pet_id, personal_info_id):
    new_questionnaire = Questionnaire(pet_id=pet_id, personal_info_id=personal_info_id)
    db.session.add(new_questionnaire)
    db.session.commit()
    return new_questionnaire | None


def add_pet_to_shelter(name, gender, breed, age, is_sterilized, size, species_id, image, description):
    new_pet = Pet(
        name=name,
        gender=gender,
        breed=breed,
        age=age,
        is_sterilized=is_sterilized,
        size=size,
        species_id=species_id,
        image=image,
        description=description,
        in_shelter=False
    )

    db.session.add(new_pet)
    db.session.commit()
    return new_pet
