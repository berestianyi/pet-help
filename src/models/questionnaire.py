from src import db
from src.models.user import User
from sqlalchemy import Enum, ForeignKey, Column, Integer, String


class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    questionnaires = db.relationship('Questionnaire', backref='personal_info', lazy=True)


class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personal_info_id = db.Column(db.Integer, db.ForeignKey('personal_info.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    pet = db.relationship('Pet', backref='questionnaires')
