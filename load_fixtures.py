import json
import os

from src import app, db
from src.models import Species, Pet, PetGender, PetSize, PetStatus

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


def clear_data():

    with app.app_context():
        db.session.query(Pet).delete()
        db.session.query(Species).delete()
        db.session.commit()


def load_fixtures_json():
    with app.app_context():
        clear_data()

        with open(os.path.join(FIXTURES_DIR, 'species.json'), 'r') as file:
            species_data = json.load(file)
            for record in species_data:
                fields = record['fields']
                species = Species(name=fields['name'], status=PetStatus(fields['status']))
                db.session.add(species)
            db.session.commit()

        with open(os.path.join(FIXTURES_DIR, 'pet.json'), 'r') as file:
            pet_data = json.load(file)
            for record in pet_data:
                fields = record['fields']
                pet = Pet(
                    name=fields['name'],
                    breed=fields['breed'],
                    gender=PetGender(fields['gender']),
                    age=fields['age'],
                    is_sterilized=fields['is_sterilized'],
                    size=PetSize(fields['size']),
                    species_id=fields['species_id'],
                    image=fields['image'],
                    description=fields['description'],
                    status=PetStatus(fields['status']),
                )
                db.session.add(pet)
            db.session.commit()


if __name__ == '__main__':
    load_fixtures_json()
