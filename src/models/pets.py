import enum

from flask_admin.contrib.sqla import ModelView
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

    def __init__(self, name, gender, age, is_sterilized, size, species):
        self.name = name
        self.gender = gender
        self.age = age
        self.is_sterilized = is_sterilized
        self.size = size
        self.species = species

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'breed': self.breed,
            'gender': self.gender.value,
            'age': self.age,
            'is_sterilized': self.is_sterilized,
            'size': self.size.value,
            'species_id': self.species_id if self.species_id else None
        }


class PetView(ModelView):
    form_columns = ['name', 'breed', 'gender', 'age', 'is_sterilized', 'size', 'species']


admin.add_view(PetView(Pet, db.session))
