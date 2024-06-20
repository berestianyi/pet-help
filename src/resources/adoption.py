from flask import render_template, make_response, request, redirect, url_for
from flask_login import current_user
from flask_restful import Resource

from src import csrf, db
from src.models import Pet, Species, PetGender, PetSize
from src import models
from src.utils.validation.validation import Validation


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
        'species': False,
        'breeds': False,
        'genders': False,
        'sizes': False,
        'ages': False,
        'sterilized': False
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
        species = [s.name for s in Species.query.all()]
        breeds = [p.breed for p in Pet.query.all()]
        genders, sizes = list(PetGender), list(PetSize)
        page = request.form.get('page_num', 1, type=int)
        per_page = request.form.get('per_page', 6, type=int)

        query = Pet.query
        total_pets = query.count()

        pagination = {
            'total_pages': -(-total_pets // per_page),
            'current_page': page,
            'has_next': page < -(-total_pets // per_page),
            'has_prev': page > 1,
            'next_num': page + 1 if page < -(-total_pets // per_page) else None,
            'prev_num': page - 1 if page > 1 else None,
            'show': total_pets > 6
        }

        pets = query.offset((page - 1) * per_page).limit(per_page).all()
        user = current_user

        personal_info = (
            models.PersonalInfo.query.filter_by(id=user.personal_info_id).first()
            if user.is_authenticated else None
        )

        full_name = personal_info.full_name if personal_info else ''
        phone = personal_info.phone if personal_info else ''
        description = personal_info.description if personal_info else ''
        birth_date = personal_info.birth_date.strftime('%m/%d/%Y') if personal_info else ''
        personal_info_disabled = 'disabled' if personal_info else ''

        selected_input = {
            'specie': 'All species',
            'gender': 'All genders',
            'size': 'All sizes',
            'age': 'All ages',
            'sterilize': 'Sterilized?',
            'breed': 'All breeds',
        }

        return make_response(render_template(
            'adoption/adoption.html',
            pets=pets,
            pets_id=[pet.id for pet in pets],
            species=species,
            sizes=sizes,
            breeds=breeds,
            genders=genders,
            ages=self.ages,
            sterilized=self.sterilized,
            selected=selected_input,
            html_option=self.html_all_option,
            pagination=pagination,
            user=user,
            full_name=full_name,
            phone=phone,
            description=description,
            birth_date=birth_date,
            personal_info_disabled=personal_info_disabled,
            submit_button_disabled='disabled'
        ))

    def post(self):
        full_name, description = request.form.get('fullName'), request.form.get('description')
        birth_date, phone = request.form.get('datepicker'), request.form.get('phoneNumber')
        pet_id = request.form.get('selectedCardId')
        user = current_user

        try:
            personal_info = (
                models.PersonalInfo.query.filter_by(id=user.personal_info_id).first()
                if user.is_authenticated else None
            )

            if not personal_info:
                personal_info = models.PersonalInfo(
                    full_name=full_name, phone=phone, description=description, birth_date=birth_date
                )
                db.session.add(personal_info)
                db.session.commit()
                if user.is_authenticated:
                    user.personal_info_id = personal_info.id
                    db.session.commit()

            questionnaire = models.Questionnaire(pet_id=pet_id, personal_info_id=personal_info.id)
            db.session.add(questionnaire)
            db.session.commit()
        except:

            return redirect(url_for('questionnaire'))

        return make_response(render_template('adoption/thank_you.html'))


class Info(Resource):
    method_decorators = [csrf.exempt]

    def post(self):
        pets = request.form.getlist('pets')

        pet_ids = [int(pet) for pet in pets]
        print(pet_ids)
        print(request.form)


class QuestionnaireHTMX(Resource, DataMixin):
    method_decorators = [csrf.exempt]

    def post(self):
        print(request.form)
        pet_id = request.form.get('selectedCardId')
        full_name = request.form.get('fullName')
        phone = request.form.get('phoneNumber')
        description = request.form.get('description')
        birth_date = request.form.get('datepicker')
        specie = request.form.get('species')
        gender = request.form.get('genders')
        size = request.form.get('sizes')
        age = request.form.get('ages')
        sterilize = request.form.get('sterilized')
        breed = request.form.get('breeds')
        page = request.form.get('page_num', 1, type=int)
        per_page = int(request.form.get('per_page', 6, type=int))

        species_list = self.species_filter(specie)
        genders_list = self.genders_filter(gender)
        sizes_list = self.sizes_filter(size)
        ages_list = self.ages_filter(age)
        sterilizes_list = self.sterilized_filter(sterilize)
        breed, breeds_list = self.breeds_filter(breed, specie)

        user = current_user
        personal_info = (
            models.PersonalInfo.query.filter_by(id=user.personal_info_id).first()
            if user.is_authenticated else None
        )

        if personal_info is None:
            birth_date_error = Validation.date_format(birth_date)
        else:
            birth_date_error = None

        personal_info_disabled = 'disabled' if personal_info else ''

        if personal_info:
            full_name = personal_info.full_name
            phone = personal_info.phone
            description = personal_info.description
            birth_date = personal_info.birth_date.strftime('%m/%d/%Y')

        query = Pet.query
        query = self.query_filter(query, specie, gender, size, age, sterilize, breed)
        total_pets = query.count()

        submit_button_disabled = 'disabled'

        if all([
            Validation.date_format(birth_date) is None,
            Validation.correct_phone_number(phone) is None,
            Validation.at_least_3_chars(description) is None,
            Validation.at_least_3_chars(full_name) is None,
        ]):
            submit_button_disabled = ''

        pagination = {
            'total_pages': -(-total_pets // per_page),
            'current_page': page,
            'has_next': page < -(-total_pets // per_page),
            'has_prev': page > 1,
            'next_num': page + 1 if page < -(-total_pets // per_page) else None,
            'prev_num': page - 1 if page > 1 else None,
            'show': total_pets > 6
        }

        selected_input = {
            'specie': specie,
            'gender': gender,
            'size': size,
            'age': age,
            'sterilize': sterilize,
            'breed': breed,
        }

        pets = query.offset((page - 1) * per_page).limit(per_page).all()

        return make_response(render_template(
            'adoption/questionnaire.html',
            pets=pets,
            pets_id=[pet.id for pet in pets],
            page_num=page,
            pagination=pagination,
            html_option=self.html_all_option,
            selected=selected_input,
            breeds=breeds_list,
            species=species_list,
            sizes=sizes_list,
            genders=genders_list,
            ages=ages_list,
            sterilized=sterilizes_list,
            birth_date_str=birth_date_error,
            birth_date=birth_date,
            description=description,
            full_name=full_name,
            phone=phone,
            personal_info_disabled=personal_info_disabled,
            submit_button_disabled=submit_button_disabled

        ))
