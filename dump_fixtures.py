import os
import yaml

from src import app, db
from src.models import User, PersonalInfo, Pet, Species, Questionnaire

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')
FIXTURES_FILE = os.path.join(FIXTURES_DIR, 'fixtures.yml')


def ensure_fixtures_dir():
    if not os.path.exists(FIXTURES_DIR):
        os.makedirs(FIXTURES_DIR)


def dump_fixtures_to_yaml():
    with app.app_context():
        models = [User, PersonalInfo, Pet, Species, Questionnaire]
        fixture_data = {model.__name__.lower(): [] for model in models}

        for model in models:
            records = model.query.all()
            for record in records:
                fixture_data[model.__name__.lower()].append(record.to_dict())

        with open(FIXTURES_FILE, 'w') as f:
            yaml.dump(fixture_data, f, default_flow_style=False, sort_keys=False)
        print(f"Dumped fixtures to {FIXTURES_FILE}")


if __name__ == '__main__':
    ensure_fixtures_dir()
    dump_fixtures_to_yaml()
