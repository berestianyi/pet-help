from datetime import date

from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.fields import QuerySelectField

from src import db, admin
from src.models import Pet
from src.models.user import User
from sqlalchemy import Enum, ForeignKey, Column, Integer, String


class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    age = db.Column(db.Integer, nullable=False, default=18)
    description = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    questionnaires = db.relationship('Questionnaire', backref='personal_info', lazy=True)

    def __repr__(self):
        return F'<PersonalInfo {self.full_name}>'


class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personal_info_id = db.Column(db.Integer, db.ForeignKey('personal_info.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    pet = db.relationship('Pet', backref='questionnaires')


class PersonalInfoView(ModelView):
    form_columns = ['id', 'full_name', 'age', 'description', 'phone']


admin.add_view(PersonalInfoView(PersonalInfo, db.session))


