import enum

from sqlalchemy import Enum

from src import db


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


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    breed = db.Column(db.String(80), unique=True, nullable=True)
    gender = db.Column(Enum(PetGender), nullable=False, default=PetGender.FEMALE)
    age = db.Column(db.Integer, nullable=False)
    is_sterilized = db.Column(db.Boolean, nullable=False, default=False)
    size = db.Column(Enum(PetSize), nullable=False, default=PetSize.MEDIUM)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)

    def __init__(self, name, gender, age, is_sterilized, size, species):
        self.name = name
        self.gender = gender
        self.age = age
        self.is_sterilized = is_sterilized
        self.size = size
        self.species = species


