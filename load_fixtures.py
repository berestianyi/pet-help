import json
import os
from flask_fixtures import load_fixtures

from src import app, db

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


def load_data():
    with app.app_context():

        for filename in ['species.json', 'pet.json']:
            file_path = os.path.join(FIXTURES_DIR, filename)
            with open(file_path, 'r') as file:
                content = json.load(file)
                print(f"Loaded {filename}: {content}")

        load_fixtures(db, [
            os.path.join(FIXTURES_DIR, 'species.json'),
            os.path.join(FIXTURES_DIR, 'pet.json'),
        ])


if __name__ == '__main__':
    load_data()
