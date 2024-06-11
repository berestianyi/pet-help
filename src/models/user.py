import uuid

from src import db, bcrypt
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(254), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    uuid = db.Column(db.String(36), unique=True, nullable=True, default=lambda: str(uuid.uuid4()))
    personal_info_id = db.Column(db.Integer, db.ForeignKey('personal_info.id'), nullable=True)
    personal_info = db.relationship('PersonalInfo', backref='users')

    def __init__(self, username, email, password):
        self.uuid = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }
