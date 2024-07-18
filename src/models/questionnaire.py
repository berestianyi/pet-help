from flask_admin.contrib.sqla import ModelView
from src import db, admin


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

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'birth_date': self.birth_date.isoformat(),
            'age': self.age,
            'description': self.description,
            'phone': self.phone,
            'questionnaires': [q.to_dict() for q in self.questionnaires]
        }


class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personal_info_id = db.Column(db.Integer, db.ForeignKey('personal_info.id'), nullable=False)
    pet_id = db.Column(db.Integer, db.ForeignKey('pet.id'), nullable=False)
    pet = db.relationship('Pet', backref='questionnaires')

    def to_dict(self):
        return {
            'id': self.id,
            'personal_info_id': self.personal_info_id,
            'pet_id': self.pet_id,
            'pet': self.pet.to_dict() if self.pet else None
        }


class PersonalInfoView(ModelView):
    column_list = ['id', 'full_name', 'birth_date', 'age', 'description', 'phone']


class QuestionnaireView(ModelView):
    column_list = ['personal_info.full_name', 'personal_info.birth_date', 'personal_info.age', 'personal_info.description', 'personal_info.phone', 'pet.name']
    column_labels = {
        'personal_info.full_name': 'Full Name',
        'personal_info.birth_date': 'Birth Date',
        'personal_info.age': 'Age',
        'personal_info.description': 'Description',
        'personal_info.phone': 'Phone',
        'pet.name': 'Pet Name'
    }


admin.add_view(PersonalInfoView(PersonalInfo, db.session))
admin.add_view(QuestionnaireView(Questionnaire, db.session))