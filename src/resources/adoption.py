from flask import render_template, make_response, request
from flask_restful import Resource

from src import csrf
from src.models import Pet, Species, PetGender, PetSize


class DataMixin:
    ages = {
        '0-3': (0, 3),
        '4-6': (4, 6),
        '7+': (7, 30)}

    sterilized = {
        'Yes': True,
        'No': False,
    }

    html_all_option = {
        'species': True,
        'breeds': True,
        'genders': True,
        'sizes': True,
        'ages': True,
        'sterilized': True
    }

    def query_filter(self, query, specie, gender, size, age, sterilize, breed):
        if specie != 'All species':
            specie_name = Species.query.filter_by(name=specie).first()
            query = query.filter(Pet.species_id == specie_name.id)
            if breed != 'All breeds':
                query = query.filter(Pet.breed == breed)
        else:
            if breed != 'All breeds':
                query = query.filter(Pet.breed == breed)
        if gender != 'All genders':
            query = query.filter(Pet.gender == PetGender[gender.upper()])
        if size != 'All sizes':
            query = query.filter(Pet.size == PetSize[size.upper()])
        if age != 'All ages':
            age_range = self.ages.get(age)
            if age_range:
                query = query.filter(Pet.age >= age_range[0], Pet.age <= age_range[1])
        if sterilize != 'Sterilized?':
            query = query.filter(Pet.is_sterilized == self.sterilized[sterilize])
        return query

    def breeds_filter(self, breed, specie):
        if breed == 'All breeds':
            if specie == 'All species':
                breed = 'All breeds'
                breeds = [pet.breed for pet in Pet.query.all()]
            else:
                breeds = [pet.breed for pet in
                          Pet.query.filter(Pet.species_id == Species.query.filter_by(name=specie).first().id)]
                self.html_all_option['breeds'] = False
        else:
            if specie == 'All species':
                breeds = [pet.breed for pet in Pet.query.all()]
                breeds.remove(breed)
                breeds.append('All breeds')
            else:
                breeds = [pet.breed for pet in
                          Pet.query.filter(Pet.species_id == Species.query.filter_by(name=specie).first().id)]
                self.html_all_option['breeds'] = False
                breeds.remove(breed)
                breeds.append('All breeds')

            self.html_all_option['breeds'] = True

        return breed, breeds

    def species_filter(self, specie):
        if specie == 'All species':
            self.html_all_option['species'] = False
            species = [specie.name for specie in Species.query.all()]
        else:
            species_list = Species.query.filter(Species.name != specie).all()
            species = [specie.name for specie in species_list]
            self.html_all_option['breeds'] = False
            self.html_all_option['species'] = True
        return species

    def genders_filter(self, gender_):
        if gender_ == 'All genders':
            self.html_all_option['genders'] = False
            genders = list(PetGender)
        else:
            genders = [gender for gender in PetGender if gender != PetGender[gender_.upper()]]
            self.html_all_option['genders'] = True
        return genders

    def sizes_filter(self, size_):
        if size_ == 'All sizes':
            self.html_all_option['sizes'] = False
            sizes = list(PetSize)
        else:
            sizes = [size for size in PetSize if size != PetSize[size_.upper()]]
            self.html_all_option['sizes'] = True
        return sizes

    def ages_filter(self, age):
        if age == 'All ages':
            self.html_all_option['ages'] = False
            new_ages = self.ages.copy()
        else:
            self.html_all_option['ages'] = True
            new_ages = self.ages.copy()
            new_ages.pop(age, None)
        return new_ages

    def sterilized_filter(self, sterilize):
        if sterilize == 'Sterilized?':
            self.html_all_option['sterilized'] = False
            new_sterilized = self.sterilized.copy()
        else:
            self.html_all_option['sterilized'] = True
            new_sterilized = self.sterilized.copy()
            new_sterilized.pop(sterilize, None)
        return new_sterilized


class Questionnaire(Resource, DataMixin):

    def get(self):
        pets = Pet.query.limit(6).all()
        species = Species.query.all()
        genders = list(PetGender)
        sizes = list(PetSize)

        return make_response(render_template(
            'adoption/adoption.html',
            pets=pets,
            species=species,
            sizes=sizes,
            genders=genders,
            ages=self.ages,
            sterilized=self.sterilized,
        ))

    def post(self):
        return {'questionnaire': Questionnaire()}


class FormFilter(Resource, DataMixin):
    method_decorators = [csrf.exempt]

    def post(self):
        print("FormFilter", request.form)
        specie = request.form.get('species')
        gender = request.form.get('genders')
        size = request.form.get('sizes')
        age = request.form.get('ages')
        sterilize = request.form.get('sterilized')
        breed = request.form.get('breeds')

        species_list = self.species_filter(specie)
        genders_list = self.genders_filter(gender)
        sizes_list = self.sizes_filter(size)
        ages_list = self.ages_filter(age)
        sterilizes_list = self.sterilized_filter(sterilize)
        breed, breeds_list = self.breeds_filter(breed, specie)

        return make_response(render_template(
            'adoption/htmx/pet_filter.html',
            breeds=breeds_list,
            breed=breed,
            specie=specie,
            gender=gender,
            size=size,
            species=species_list,
            sizes=sizes_list,
            genders=genders_list,
            age=age,
            ages=ages_list,
            sterilize=sterilize,
            sterilized=sterilizes_list,
            html_option=self.html_all_option
        ))


class PetsCards(Resource, DataMixin):
    method_decorators = [csrf.exempt]

    def post(self):
        specie = request.form.get('species')
        gender = request.form.get('genders')
        size = request.form.get('sizes')
        age = request.form.get('ages')
        sterilize = request.form.get('sterilized')
        breed = request.form.get('breeds')

        query = Pet.query

        query = self.query_filter(query, specie, gender, size, age, sterilize, breed)

        try:
            pets = query.limit(6).all()
        except:
            pets = None

        return make_response(render_template(
            'adoption/htmx/pet_cards.html',
            pets=pets))


class SpeciesFilter(Resource):
    def get(self):
        specie = request.args.get('species')
        try:
            specie_pets = Pet.query.filter_by(species_id=specie).all()
        except:
            return make_response(render_template('adoption/htmx/empty_breed_filter.html'))
        else:
            return make_response(render_template('adoption/htmx/breed_filter.html', specie_pets=specie_pets))
