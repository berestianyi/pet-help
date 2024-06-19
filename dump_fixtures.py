import os
import json

from src import app, db
from src.models import User, PersonalInfo, Pet, Species, Questionnaire

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


def ensure_fixtures_dir():
    if not os.path.exists(FIXTURES_DIR):
        os.makedirs(FIXTURES_DIR)


def dump_fixtures():
    with app.app_context():
        models = [User, PersonalInfo, Pet, Species, Questionnaire]
        fixture_data = {model.__name__.lower(): [] for model in models}

        for model in models:
            records = model.query.all()

            for record in records:
                fixture_data[model.__name__.lower()].append({
                    "model": model.__name__,
                    "fields": record.to_dict()
                })

        for model_name, data in fixture_data.items():
            file_path = os.path.join(FIXTURES_DIR, f'{model_name}.json')
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Dumped {len(data)} records to {file_path}")


if __name__ == '__main__':
    ensure_fixtures_dir()
    dump_fixtures()
