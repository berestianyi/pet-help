import os

from werkzeug.utils import secure_filename

from src.models import Questionnaire, Pet, Species, PetGender, PetSize, PetStatus
from src import db, app


def add_questionnaire(pet_id, personal_info_id):
    new_questionnaire = Questionnaire(pet_id=pet_id, personal_info_id=personal_info_id)
    db.session.add(new_questionnaire)
    db.session.commit()
    return new_questionnaire | None


def add_pet_to_shelter(name, gender, breed, age, is_sterilized, size, species_id, image, description):

    file_path = os.path.join(app.config['UPLOAD_FOLDER_FOR_SHELTER'], image.filename)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    image.save(file_path)

    new_pet = Pet(
        name=name,
        gender=PetGender(gender),
        breed=breed,
        age=age,
        is_sterilized=False if is_sterilized == 'No' else True,
        size=PetSize(size),
        species_id=species_id,
        image='uploads/' + image.filename,
        description=description,
        status=PetStatus.PENDING
    )

    db.session.add(new_pet)
    db.session.commit()
    return new_pet


def add_specie(name):
    new_specie = Species(
        name=name, in_shelter=False
    )
    db.session.add(new_specie)
    db.session.commit()
    return new_specie


def get_specie_by_name(species_name):
    species = Species.query.filter_by(name=species_name).first()
    return species


def change_pet_status(pet_id, status: PetStatus) -> Pet:
    pet = Pet.query.filter_by(id=pet_id).first()
    pet.status = status
    db.session.commit()
    return pet
