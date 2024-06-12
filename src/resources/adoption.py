from flask import render_template, make_response, request
from flask_restful import Resource
from src.models import Pet, Species, PetGender, PetSize


class Questionnaire(Resource):

    def get(self):
        pets = Pet.query.all()
        species = Species.query.all()
        genders = list(PetGender)
        sizes = list(PetSize)
        ages = {
            '0-3': (0, 3),
            '4-6': (4, 6),
            '7+': (7, 30)}

        sterilized = {
            'Yes': True,
            'No': False,
        }
        disabled = {
            'breeds': 'disabled',
            'genders': ' ',
            'sizes': ' ',
            'ages': ' ',
            'sterilized': ' '
        }

        return make_response(render_template(
            'adoption/adoption.html',
            pets=pets,
            species=species,
            sizes=sizes,
            genders=genders,
            ages=ages,
            sterilized=sterilized,
            disabled=disabled,
        ))

    def post(self):
        return {'questionnaire': Questionnaire()}


class FormFilter(Resource):
    def post(self):
        print(request.form)
        specie_args = request.form.get('species')
        gender_args = request.form.get('genders')
        size_args = request.form.get('sizes')
        age_args = request.form.get('ages')
        sterilize_args = request.form.get('sterilized')
        breed_args = request.form.get('breeds')

        disabled_args = {
            'breeds': ' ',
            'genders': ' ',
            'sizes': ' ',
            'ages': ' ',
            'sterilized': ' '
        }

        html_option = {
            'species': True,
            'breeds': True,
            'genders': True,
            'sizes': True,
            'ages': True,
            'sterilized': True
        }

        ages = {
            '0-3': (0, 3),
            '4-6': (4, 6),
            '7+': (7, 30)}

        sterilized = {
            'Yes': True,
            'No': False,
        }

        specie_name = Species.query.filter_by(name=specie_args).first()
        query = Pet.query

        if breed_args is None or specie_args == 'All species':
            breed_args = 'All breeds'

        if not specie_args == 'All species':
            query = query.filter(Pet.species_id == specie_name.id)
            species = Species.query.filter(Species.name != specie_args).all()
        else:
            html_option['species'] = False
            disabled_args['breeds'] = 'disabled'
            species = Species.query.all()

        if breed_args == 'All breeds':
            html_option['breeds'] = False

        if not gender_args == 'All genders':
            query = query.filter(Pet.gender == PetGender[gender_args.upper()])
            genders = [gender for gender in PetGender if gender != PetGender[gender_args.upper()]]
        else:
            html_option['genders'] = False
            genders = list(PetGender)

        if not size_args == 'All sizes':
            query = query.filter(Pet.size == PetSize[size_args.upper()])
            sizes = [size for size in PetSize if size != PetSize[size_args.upper()]]
        else:
            html_option['sizes'] = False
            sizes = list(PetSize)

        if not age_args == 'All ages':
            query = query.filter(Pet.age >= ages.get(age_args)[0], Pet.age <= ages.get(age_args)[1])
            ages.pop(age_args, None)
        else:
            html_option['ages'] = False

        if not sterilize_args == 'Sterilized?':
            query = query.filter(Pet.is_sterilized == sterilize_args)
            sterilized.pop(sterilize_args, None)
        else:
            html_option['sterilized'] = False
        try:
            pets = query.all()
        except:
            pets = None

        print(pets)
        print(sterilize_args)
        print(sterilized)
        return make_response(render_template(
            'adoption/htmx/pet_filter.html',
            pets=pets,
            breed=breed_args,
            specie=specie_args,
            gender=gender_args,
            size=size_args,
            species=species,
            sizes=sizes,
            genders=genders,
            age=age_args,
            ages=ages,
            sterilize=sterilize_args,
            sterilized=sterilized,
            disabled=disabled_args,
            html_option=html_option
        ))


class SpeciesFilter(Resource):
    def get(self):
        specie = request.args.get('species')
        try:
            specie_pets = Pet.query.filter_by(species_id=specie).all()
        except:
            return make_response(render_template('adoption/htmx/empty_breed_filter.html'))
        else:
            return make_response(render_template('adoption/htmx/breed_filter.html', specie_pets=specie_pets))

