import os


from src.models import Questionnaire, Pet, Species, PetGender, PetSize, PetStatus
from src import db, app


def add_questionnaire(pet_id, personal_info_id) -> Questionnaire | None:
    new_questionnaire = Questionnaire(pet_id=pet_id, personal_info_id=personal_info_id)
    db.session.add(new_questionnaire)
    db.session.commit()
    return new_questionnaire


def add_pet_to_shelter(
        name,
        gender,
        breed,
        age,
        is_sterilized,
        size,
        species_id,
        image,
        description
) -> Pet | None:
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


def add_specie(name) -> Species | None:
    new_specie = Species(
        name=name, status=PetStatus.AVAILABLE
    )
    db.session.add(new_specie)
    db.session.commit()
    return new_specie


def get_specie_by_name(species_name) -> Species | None:
    species = Species.query.filter_by(name=species_name).first()
    return species


def change_pet_status(pet_id, status: PetStatus) -> Pet | None:
    pet = Pet.query.filter_by(id=pet_id).first()
    pet.status = status
    db.session.commit()
    return pet


def get_pet_by_id(pet_id) -> Pet:
    pet = Pet.query.filter_by(id=pet_id).first()
    return pet


class DataCrudMixin:
    ages = {
        '0-3': (0, 3),
        '4-6': (4, 6),
        '7+': (7, 30)}

    sterilized = {
        'Yes': True,
        'No': False,
    }

    def query_filter(self, query, specie, gender, size, age, sterilize, breed):
        query = query.filter(Pet.status == PetStatus.AVAILABLE)
        if specie != 'All species':
            specie_name = Species.query.filter_by(name=specie).first()
            query = query.filter(Pet.species_id == specie_name.id)
            if breed != 'All breeds':
                query = query.filter(Pet.breed == breed)
        else:
            if breed != 'All breeds':
                query = query.filter(Pet.breed == breed)
        if gender != 'All genders':
            query = query.filter(Pet.gender == PetGender[gender.upper()])
        if size != 'All sizes':
            query = query.filter(Pet.size == PetSize[size.upper()])
        if age != 'All ages':
            age_range = self.ages.get(age)
            if age_range:
                query = query.filter(Pet.age >= age_range[0], Pet.age <= age_range[1])
        if sterilize != 'Sterilized?':
            query = query.filter(Pet.is_sterilized == self.sterilized[sterilize])

        return query

    @staticmethod
    def breeds_filter(breed, specie):
        if breed == 'All breeds':
            if specie == 'All species':
                breed = 'All breeds'
                breeds = [pet.breed for pet in Pet.query.filter(Pet.status == PetStatus.AVAILABLE)]
            else:
                breeds = [pet.breed for pet in
                          Pet.query.filter(Pet.species_id == Species.query.filter_by(name=specie).first().id,
                                           Pet.status == PetStatus.AVAILABLE)]

        else:
            if specie == 'All species':
                breeds = [pet.breed for pet in Pet.query.filter(Pet.status == PetStatus.AVAILABLE)]
                breeds.remove(breed)
            else:
                breeds = [pet.breed for pet in
                          Pet.query.filter(Pet.species_id == Species.query.filter_by(
                              name=specie).first().id, Pet.status == PetStatus.AVAILABLE)]
                breeds.remove(breed)
            breeds.append('All breeds')

        return breed, breeds

    @staticmethod
    def species_filter(specie, additional_word):
        if specie == additional_word:
            species = [specie.name for specie in Species.query.all()]
        else:
            species_list = Species.query.filter(Species.name != specie).all()
            species = [specie.name for specie in species_list]
            species.append(additional_word)
        return species

    @staticmethod
    def genders_filter(gender_, additional_word):
        if gender_ == additional_word:
            genders = [gender.value for gender in PetGender]
        else:
            genders = [gender.value for gender in PetGender if gender.value != gender_]
            genders.append(additional_word)
        return genders

    @staticmethod
    def sizes_filter(size_, additional_word):
        if size_ == additional_word:
            sizes = [size.value for size in PetSize]
        else:
            sizes = [size.value for size in PetSize if size.value != size_]
            sizes.append(additional_word)
        return sizes

    def ages_filter(self, age, additional_word):
        if age == additional_word:
            new_ages = self.ages.copy()
        else:
            new_ages = self.ages.copy()
            new_ages.pop(age, None)
            new_ages.update({additional_word: additional_word})
        return new_ages

    def sterilized_filter(self, sterilize, additional_word):
        if sterilize == additional_word:
            new_sterilized = self.sterilized.copy()
        else:
            new_sterilized = self.sterilized.copy()
            new_sterilized.pop(sterilize, None)
            new_sterilized.update({additional_word: additional_word})
        return new_sterilized

    @staticmethod
    def paginate(total_pets, page, per_page) -> dict:
        return {
            'total_pages': -(-total_pets // per_page),
            'next_num': page + 1 if page < -(-total_pets // per_page) else None,
            'has_next': page < -(-total_pets // per_page),
        }

    @staticmethod
    def empty_string(value):
        return '' if value is None else value

