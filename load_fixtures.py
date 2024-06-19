import os

import yaml
from flask_fixtures import load_fixtures

from src import app, db

FIXTURES_FILE = os.path.join(os.path.dirname(__file__), 'fixtures.yml')


def load_yaml_fixtures():
    with open(FIXTURES_FILE, 'r') as f:
        fixtures = yaml.safe_load(f)

    with app.app_context():
        load_fixtures(db, fixtures)
        print("Fixtures loaded successfully.")


if __name__ == '__main__':
    load_yaml_fixtures()
