import enum
import os

from flask_admin.contrib.sqla import ModelView
from flask_admin.form.upload import ImageUploadField
from sqlalchemy import Enum

from src import db, admin
from src.utils.utils import text_to_slug


class PetSize(enum.Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class PetGender(enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class PetStatus(enum.Enum):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    ADOPTED = "ADOPTED"
    BOOKED = "BOOKED"


class Species(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    pets = db.relationship('Pet', back_populates='species', lazy=True)
    status = db.Column(Enum(PetStatus), nullable=True, default=PetStatus.PENDING)

    def __repr__(self):
        return f'<Species {self.name}>'

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'status': self.status.value,
        }

    def __init__(self, name, status):
        self.name = name
        self.status = status


class Pet(db.Model):
    """

    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    breed = db.Column(db.String(80), unique=True, nullable=True)
    gender = db.Column(Enum(PetGender), nullable=False, default=PetGender.FEMALE)
    age = db.Column(db.Integer, nullable=False)
    is_sterilized = db.Column(db.Boolean, nullable=False, default=False)
    size = db.Column(Enum(PetSize), nullable=False, default=PetSize.MEDIUM)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)
    species = db.relationship('Species',  back_populates='pets', lazy=True)
    slug = db.Column(db.String(90), unique=True, nullable=True)
    image = db.Column(db.String(300), nullable=True)
    description = db.Column(db.String(300), nullable=True)
    status = db.Column(Enum(PetStatus), nullable=True, default=PetStatus.PENDING)

    def __init__(self, name, gender, age, is_sterilized, size, species_id, breed, image, description):
        self.name = name
        self.gender = gender
        self.breed = breed
        self.age = age
        self.is_sterilized = is_sterilized
        self.size = size
        self.species_id = species_id
        self.image = image
        self.description = description
        self.slug = text_to_slug(name + breed)

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
            'image': self.image,
            'description': self.description,
            'status': self.status.value,
            'slug': self.slug,
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

    form_columns = ['name', 'breed', 'gender', 'age', 'is_sterilized', 'size', 'species', 'image', 'description', 'status']


admin.add_view(PetView(Pet, db.session))
