import enum
import os

from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from sqlalchemy import Enum

from src import db, admin


class PetSize(enum.Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class PetGender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    pets = db.relationship('Pet', backref='specie s', lazy=True)

    def __repr__(self):
        return f'<Species {self.name}>'

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    breed = db.Column(db.String(80), unique=True, nullable=True)
    gender = db.Column(Enum(PetGender), nullable=False, default=PetGender.FEMALE)
    age = db.Column(db.Integer, nullable=False)
    is_sterilized = db.Column(db.Boolean, nullable=False, default=False)
    size = db.Column(Enum(PetSize), nullable=False, default=PetSize.MEDIUM)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)
    species = db.relationship('Species', backref='pet', lazy=True)
    image = db.Column(db.String(300), nullable=True)

    def __init__(self, pk, name, gender, age, is_sterilized, size, species_id, breed, image):
        self.id = pk
        self.name = name
        self.gender = gender
        self.breed = breed
        self.age = age
        self.is_sterilized = is_sterilized
        self.size = size
        self.species_id = species_id,
        self.image = image

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'breed': self.breed,
            'gender': self.gender.value,
            'age': self.age,
            'is_sterilized': self.is_sterilized,
            'size': self.size.value,
            'species_id': self.species_id if self.species_id else None,
            'image': self.image
        }


class PetView(ModelView):
    file_path = os.path.join(os.path.dirname(__file__), '../static')

    if not os.path.exists(file_path):
        os.makedirs(file_path)

    form_extra_fields = {
        'image': ImageUploadField('Image',
                                  base_path=file_path,
                                  relative_path='uploads/',
                                  thumbnail_size=(100, 100, True))
    }

    form_columns = ['name', 'breed', 'gender', 'age', 'is_sterilized', 'size', 'species', 'image']


admin.add_view(PetView(Pet, db.session))
