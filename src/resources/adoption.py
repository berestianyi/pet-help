from flask import render_template, make_response, request
from flask_login import login_required
from flask_restful import Resource

from src import app
from src.models import Pet, Species, PetGender, PetSize


class Questionnaire(Resource):

    def get(self):
        pets = Pet.query.all()
        species = Species.query.all()
        genders = list(PetGender)
        sizes = list(PetSize)
        return make_response(render_template(
            'adoption/adoption.html',
            pets=pets,
            species=species,
            sizes=sizes,
            genders=genders
        ))

    def post(self):
        return {'questionnaire': Questionnaire()}


class FormFilter(Resource):
    def post(self):
        pass


@app.route('/form/filter/breeds', methods=['GET'])
def filter_breeds():
    specie = request.args.get('species')
    print(specie)
    specie_pets = Pet.query.filter_by(species_id=specie).all()
    return make_response(render_template('adoption/htmx/breed_filter.html', specie_pets=specie_pets))
