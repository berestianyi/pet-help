import os
from flask_fixtures import load_fixtures

from src import app, db

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


def load_data():
    with app.app_context():
        load_fixtures(db, [
            os.path.join(FIXTURES_DIR, 'user.json'),
            os.path.join(FIXTURES_DIR, 'personalinfo.json'),
            os.path.join(FIXTURES_DIR, 'pet.json'),
            os.path.join(FIXTURES_DIR, 'species.json'),
            os.path.join(FIXTURES_DIR, 'questionnaire.json')
        ])


if __name__ == '__main__':
    load_data()
