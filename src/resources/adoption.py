from flask import render_template, make_response, request, redirect, url_for, send_from_directory, flash
from flask_login import current_user
from flask_restful import Resource

from src import csrf, app, ALLOWED_EXTENSIONS
from src.models import Pet, Species, PetGender, PetSize
from src.utils.validation.validation import Validation, validate_give_shelter_form, validate_image_format

from src import crud


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory('static', filename)


class DataMixin:
    ages = {
        '0-3': (0, 3),
        '4-6': (4, 6),
        '7+': (7, 30)}

    sterilized = {
        'Yes': True,
        'No': False,
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

    @staticmethod
    def breeds_filter(breed, specie):
        if breed == 'All breeds':
            if specie == 'All species':
                breed = 'All breeds'
                breeds = [pet.breed for pet in Pet.query.all()]
            else:
                breeds = [pet.breed for pet in
                          Pet.query.filter(Pet.species_id == Species.query.filter_by(name=specie).first().id)]

        else:
            if specie == 'All species':
                breeds = [pet.breed for pet in Pet.query.all()]
                breeds.remove(breed)
                breeds.append('All breeds')
            else:
                breeds = [pet.breed for pet in
                          Pet.query.filter(Pet.species_id == Species.query.filter_by(name=specie).first().id)]
                breeds.remove(breed)
                breeds.append('All breeds')

            breeds.append('All breeds')

        return breed, breeds

    @staticmethod
    def species_filter(specie, additional_word):
        if specie == additional_word:
            species = [specie.name for specie in Species.query.all()]
        else:
            species_list = Species.query.filter(Species.name != specie).all()
            species = [specie.name for specie in species_list]
            species.append(additional_word)
        return species

    @staticmethod
    def genders_filter(gender_, additional_word):
        if gender_ == additional_word:
            genders = [gender.value for gender in PetGender]
        else:
            genders = [gender.value for gender in PetGender if gender.value != gender_]
            genders.append(additional_word)
        return genders

    @staticmethod
    def sizes_filter(size_, additional_word):
        if size_ == additional_word:
            sizes = [size.value for size in PetSize]
        else:
            sizes = [size.value for size in PetSize if size.value != size_]
            sizes.append(additional_word)
        return sizes

    def ages_filter(self, age, additional_word):
        if age == additional_word:
            new_ages = self.ages.copy()
        else:
            new_ages = self.ages.copy()
            new_ages.pop(age, None)
            new_ages.update({additional_word: additional_word})
        return new_ages

    def sterilized_filter(self, sterilize, additional_word):
        if sterilize == additional_word:
            new_sterilized = self.sterilized.copy()
        else:
            new_sterilized = self.sterilized.copy()
            new_sterilized.pop(sterilize, None)
            new_sterilized.update({additional_word: additional_word})
        return new_sterilized

    @staticmethod
    def paginate(total_pets, page, per_page) -> dict:
        return {
            'total_pages': -(-total_pets // per_page),
            'current_page': page,
            'has_next': page < -(-total_pets // per_page),
            'has_prev': page > 1,
            'next_num': page + 1 if page < -(-total_pets // per_page) else None,
            'prev_num': page - 1 if page > 1 else None,
            'show': total_pets > 6
        }

    @staticmethod
    def empty_string(value):
        return '' if value is None else value


class Questionnaire(Resource, DataMixin):

    def get(self):
        species = [s.name for s in Species.query.all()]
        breeds = [p.breed for p in Pet.query.all()]
        genders, sizes = [gender.value for gender in PetGender], [size.value for size in PetSize]
        page = request.form.get('page_num', 1, type=int)
        per_page = request.form.get('per_page', 6, type=int)

        query = Pet.query
        total_pets = query.count()

        pagination = self.paginate(total_pets, page, per_page)

        pets = query.offset((page - 1) * per_page).limit(per_page).all()
        pet_status_list = [
            {"id": pet.id, "name": pet.name, "age": pet.age,
             "image": pet.image, "size": pet.size.value, "gender": pet.gender.value,
             "sterilized": "Sterilized" if pet.is_sterilized else "Not sterilized",
             "checked": ""} for pet in pets]

        user = current_user

        personal_info = crud.get_personal_info(user=user)

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
            pets=pet_status_list,
            pets_id=[pet.id for pet in pets],
            species=species,
            sizes=sizes,
            breeds=breeds,
            genders=genders,
            ages=self.ages,
            sterilized=self.sterilized,
            selected=selected_input,
            pagination=pagination,
            user=user,
            full_name=full_name,
            phone=phone,
            description=description,
            birth_date=birth_date,
            personal_info_disabled=personal_info_disabled,
            submit_button_disabled='disabled',
        ))

    def post(self):
        full_name, description = request.form.get('fullName'), request.form.get('description')
        birth_date, phone = request.form.get('datepicker'), request.form.get('phoneNumber')
        pet_id = request.form.get('selectedCardId')
        user = current_user

        try:
            personal_info = crud.get_personal_info(user=user)

            if not personal_info:
                personal_info = crud.add_personal_info(user=user, full_name=full_name, description=description,
                                                       phone=phone, birth_date=birth_date)

            crud.add_questionnaire(pet_id=pet_id, personal_info_id=personal_info.id)

        except Exception as e:
            print(e)
            return redirect(url_for('questionnaire'))

        return make_response(render_template('adoption/thank_you.html'))


class QuestionnaireHTMX(Resource, DataMixin):
    method_decorators = [csrf.exempt]

    def post(self):
        print(request.form)
        pet_id = request.form.get('selectedCard')
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

        species_list = self.species_filter(specie, 'All species')
        genders_list = self.genders_filter(gender, 'All genders')
        sizes_list = self.sizes_filter(size, 'All sizes')
        ages_list = self.ages_filter(age, 'All ages')
        sterilizes_list = self.sterilized_filter(sterilize, 'Sterilized?')
        breed, breeds_list = self.breeds_filter(breed, specie)

        user = current_user

        personal_info = crud.get_personal_info(user=user)

        if personal_info is None:
            birth_date_error = Validation.date_format(birth_date)
        else:
            birth_date_error = None

        personal_info_disabled = 'disabled' if personal_info else ''

        if personal_info:
            full_name, phone, description, birth_date = crud.get_personal_info_fields(personal_info)

        query = Pet.query
        query = self.query_filter(query, specie, gender, size, age, sterilize, breed)
        total_pets = query.count()

        submit_button_disabled = 'disabled'

        if all([
            Validation.date_format(birth_date) is None,
            Validation.correct_phone_number(phone) is None,
            Validation.at_least_3_chars(description) is None,
            Validation.at_least_3_chars(full_name) is None,
            pet_id is not None
        ]):
            submit_button_disabled = ''

        pagination = self.paginate(total_pets, page, per_page)

        selected_input = {
            'specie': specie,
            'gender': gender,
            'size': size,
            'age': age,
            'sterilize': sterilize,
            'breed': breed,
        }

        pets = query.offset((page - 1) * per_page).limit(per_page).all()

        if pet_id is None:
            pet_id = 0

        pet_status_list = [
            {"id": pet.id, "name": pet.name, "age": pet.age,
             "image": pet.image, "size": pet.size.value, "gender": pet.gender.value,
             "sterilized": "Sterilized" if pet.is_sterilized else "Not sterilized",
             "checked": "checked" if pet.id == int(pet_id) else ""}
            for pet in pets]

        return make_response(render_template(
            'adoption/questionnaire.html',
            pets=pet_status_list,
            pets_id=[pet.id for pet in pets],
            page_num=page,
            pagination=pagination,
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
            submit_button_disabled=submit_button_disabled,
        ))


class GiveShelter(Resource, DataMixin):

    def get(self):
        species = Species.query.all()
        species_list = [specie.name for specie in species]
        species_list.append('Not in list')
        size_list = [size.value for size in PetSize]
        gender_list = [gender.value for gender in PetGender]

        selected = {
            'specie': 'Specie',
            'gender': 'Gender',
            'size': 'Size',
            'sterilized': 'Sterilized?',
        }

        is_specie_exist = True

        return make_response(render_template(
            'adoption/give_a_shelter.html',
            species=species_list,
            sizes=size_list,
            genders=gender_list,
            sterilizeds=self.sterilized,
            age=0,
            selected=selected,
            is_specie_exist=is_specie_exist,
            pet_name='',
            new_specie='',
            description='',
            file='',
            range=0,
            pet_breed=''
        ))

    def post(self):
        value = request.form

        if value['petName'] == 'Not in list':
            specie = crud.add_specie(value['newSpecie'])
        else:
            specie = crud.get_specie_by_name(value['specie'])
        print(request.files['file'])
        print(request.files['file'].filename)
        if validate_image_format(request.files['file'].filename):
            crud.add_pet_to_shelter(
                name=value['petName'],
                breed=value['petBreed'],
                size=value['size'],
                image=request.files['file'],
                species_id=specie.id,
                gender=value['gender'],
                age=value['range'],
                is_sterilized=value['sterilized'],
                description=value['description'],
            )
            return redirect(url_for('mainpage'))
        else:
            flash('Wrong image format')
            return redirect(url_for('giveshelter'))


class GiveShelterHTMX(Resource, DataMixin):
    def post(self):
        value = request.form
        print(value)

        species_list = self.species_filter(value.get('specie'), 'Specie')
        if value.get('specie') != 'Not in list':
            species_list.append('Not in list')

        selected = {
            'specie': value.get('specie'),
            'gender': value.get('gender'),
            'size': value.get('size'),
            'sterilized': value.get('sterilized'),
        }

        if value.get('specie') == 'Not in list':
            is_specie_exist = False
        else:
            is_specie_exist = True

        return make_response(render_template(
            'adoption/htmx/shelter_form.html',
            is_specie_exist=is_specie_exist,
            age=value.get('age'),
            selected=selected,
            pet_name=self.empty_string(value.get('petName')),
            pet_breed=self.empty_string(value.get('petBreed')),
            new_specie=self.empty_string(value.get('newSpecie')),
            range=0 if value.get('range') is None else value.get('range'),
            description=self.empty_string(value.get('description')),
            sterilizeds=self.sterilized_filter(value.get('sterilized'), 'Sterilized?'),
            sizes=self.sizes_filter(value.get('size'), 'Size'),
            species=species_list,
            genders=self.genders_filter(value.get('gender'), 'Gender')
        ))


class GiveShelterButtonSubmitHTMX(Resource, DataMixin):
    def post(self):
        value = request.form
        if value.get('specie') == 'Not in list':
            specie = value.get('newSpecie')
        else:
            specie = value.get('specie')

        validation_results = validate_give_shelter_form(
            name=self.empty_string(value.get('petName')),
            age=self.empty_string(value.get('range')),
            size=self.empty_string(value.get('size')),
            gender=self.empty_string(value.get('gender')),
            sterilized=self.empty_string(value.get('sterilized')),
            description=self.empty_string(value.get('description')),
            breed=self.empty_string(value.get('petBreed')),
            specie=self.empty_string(specie),
        )
        print(validation_results)
        submit_button = False

        if all(result is None for result in validation_results):
            submit_button = True

        return make_response(render_template('adoption/htmx/submit_button.html', submit_button=submit_button))
