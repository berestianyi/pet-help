from src.models import Questionnaire, Pet, Species, PetGender, PetSize
from src import db, photos


def add_questionnaire(pet_id, personal_info_id):
    new_questionnaire = Questionnaire(pet_id=pet_id, personal_info_id=personal_info_id)
    db.session.add(new_questionnaire)
    db.session.commit()
    return new_questionnaire | None


def add_pet_to_shelter(name, gender, breed, age, is_sterilized, size, species_id, image, description):

    if image and photos.file_allowed(image, image.filename):
        image = photos.save(image)

    new_pet = Pet(
        name=name,
        gender=PetGender(gender),
        breed=breed,
        age=age,
        is_sterilized=is_sterilized,
        size=PetSize(size),
        species_id=species_id,
        image=image,
        description=description,
        in_shelter=False
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
