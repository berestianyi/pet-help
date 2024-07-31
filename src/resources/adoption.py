from flask import render_template, make_response, request, redirect, url_for, send_from_directory, flash, current_app
from flask_login import current_user, login_required
from flask_restful import Resource

from src import csrf, app
from src.crud.adoption import DataCrudMixin
from src.models import Pet, Species, PetGender, PetSize, PetStatus
from src.utils.validation.validation import validate_give_shelter_form, validate_image_format

from src import crud


@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory('static', filename)


class Questionnaire(Resource, DataCrudMixin):
    """
            Resource for handling pet questionnaire forms and displaying available pets.
            """

    @login_required
    def get(self):
        """
                        Handles GET requests to display the pet questionnaire form with available pets.

                        :return: Renders the pet questionnaire template with pet data and filters.
                        """
        species = [s.name for s in Species.query.all()]
        breeds = [p.breed for p in Pet.query.filter(Pet.status == PetStatus.AVAILABLE)]
        genders, sizes = [gender.value for gender in PetGender], [size.value for size in PetSize]
        page = request.form.get('page_num', 1, type=int)
        per_page = request.form.get('per_page', 6, type=int)

        query = Pet.query.filter(Pet.status == PetStatus.AVAILABLE)
        total_pets = query.count()

        pagination = self.paginate(total_pets, page, per_page)

        pets = query.limit(page * per_page).all()

        pet_status_list = [
            {"id": pet.id, "name": pet.name, "age": pet.age,
             "image": pet.image, "size": pet.size.value, "gender": pet.gender.value,
             "sterilized": "Sterilized" if pet.is_sterilized else "Not sterilized",
             "checked": "", "description": pet.description, "breed": pet.breed, "specie": pet.species} for pet in pets]

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
        ))

    @login_required
    def post(self):
        return make_response(render_template('adoption/thank_you.html'))


class QuestionnaireHTMX(Resource, DataCrudMixin):
    method_decorators = [csrf.exempt]
    """
            Resource for handling HTMX-based questionnaire submissions and filtering pets.
            """

    def post(self):
        """
                       Handles POST requests to filter pets based on questionnaire form inputs.

                       :return: Renders the filtered pet list template with updated pet data.
                       """

        pet_id = request.form.get('selectedCard')
        specie = request.form.get('species')
        gender = request.form.get('genders')
        size = request.form.get('sizes')
        age = request.form.get('ages')
        sterilize = request.form.get('sterilized')
        breed = request.form.get('breeds')
        page = request.form.get('page_num', 1, type=int)
        per_page = request.form.get('per_page', 6, type=int)

        species_list = self.species_filter(specie, 'All species')
        genders_list = self.genders_filter(gender, 'All genders')
        sizes_list = self.sizes_filter(size, 'All sizes')
        ages_list = self.ages_filter(age, 'All ages')
        sterilizes_list = self.sterilized_filter(sterilize, 'Sterilized?')
        breed, breeds_list = self.breeds_filter(breed, specie)

        query = Pet.query
        query = self.query_filter(query, specie, gender, size, age, sterilize, breed)
        total_pets = query.count()

        pagination = self.paginate(total_pets, page, per_page)

        pets = query.limit(page * per_page).all()

        selected_input = {
            'specie': specie,
            'gender': gender,
            'size': size,
            'age': age,
            'sterilize': sterilize,
            'breed': breed,
        }

        if pet_id is None:
            pet_id = 0

        pet_status_list = [
            {"id": pet.id,
             "name": pet.name,
             "age": pet.age,
             "image": pet.image,
             "size": pet.size.value,
             "gender": pet.gender.value,
             "sterilized": "Sterilized" if pet.is_sterilized else "Not sterilized",
             "checked": "checked" if pet.id == int(pet_id) else "",
             "description": pet.description,
             "breed": pet.breed,
             "specie": pet.species}
            for pet in pets]

        return make_response(render_template(
            'adoption/questionnaire.html',
            pets=pet_status_list,
            pets_id=[pet.id for pet in pets],
            selected=selected_input,
            breeds=breeds_list,
            species=species_list,
            sizes=sizes_list,
            genders=genders_list,
            ages=ages_list,
            sterilized=sterilizes_list,
            pagination=pagination
        ))


class GiveShelter(Resource, DataCrudMixin):
    """
            Resource for handling shelter form submissions and displaying the shelter form.
            """

    @login_required
    def get(self):
        """
                        Handles GET requests to display the shelter form.

                        :return: Renders the shelter form template with relevant data.
                        """
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

    @login_required
    def post(self):
        """
                        Handles POST requests to submit the shelter form.

                        :return: Redirects to the main page or back to the shelter form with an error message.
                        """
        value = request.form

        if value['petName'] == 'Not in list':
            specie = crud.add_specie(value['newSpecie'])
        else:
            specie = crud.get_specie_by_name(value['specie'])

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


class GiveShelterHTMX(Resource, DataCrudMixin):
    """
            Resource to handle shelter form submissions via HTMX.
        """
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


class GiveShelterButtonSubmitHTMX(Resource, DataCrudMixin):
    """
            Resource to handle the submission of the shelter form button via HTMX.
            """
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

        if all(result is None for result in validation_results) and value.get('file') is not None:
            submit_button = True

        return make_response(render_template('adoption/htmx/submit_button.html', submit_button=submit_button))


class Adopt(Resource):
    """
        Resource for handling pet adoption requests.
        """
    method_decorators = [csrf.exempt]

    def get(self, pet_id):
        """
                        Handles the GET request to view a pet's adoption page.

                        :param pet_id: The ID of the pet to view.
                        :return: Renders the pet's adoption card page.

                """
        pet = crud.get_pet_by_id(pet_id)
        user = current_user

        personal_info = crud.get_personal_info(user)
        if personal_info:
            full_name, phone, description, birth_date = crud.get_personal_info_fields(personal_info)
        else:
            full_name = phone = description = birth_date = ''

        pet_status_list = {
            "id": pet.id, "name": pet.name, "age": pet.age,
            "image": pet.image, "size": pet.size.value, "gender": pet.gender.value,
            "sterilized": "Sterilized" if pet.is_sterilized else "Not sterilized",
            "checked": "", "description": pet.description, "breed": pet.breed, "specie": pet.species}

        return make_response(render_template(
            'adoption/card_page.html',
            pet=pet_status_list,
            user=user,
            full_name=full_name,
            phone=phone,
            description=description,
            birth_date=birth_date
        ))

    def post(self):
        """
                        Handles the POST request to submit an adoption application.

                        :return: Renders a thank you page upon successful submission.
                """
        try:
            full_name = request.form.get('fullName')
            phone = request.form.get('phoneNumber')
            description = request.form.get('description')
            birth_date = request.form.get('datepicker')
            pet_id = request.form.get('petId')
            user = current_user

            crud.update_personal_info(
                user=user,
                full_name=full_name,
                phone=phone,
                description=description,
                birth_date=birth_date
            )

            crud.change_pet_status(
                pet_id,
                PetStatus.ADOPTED
            )
            personal_info = crud.get_personal_info(user)

            crud.add_questionnaire(pet_id=pet_id, personal_info_id=personal_info.id)

            return make_response(render_template('adoption/thank_you.html'))
        except Exception as e:
            current_app.logger.error(f"Error in POST /adopt: {str(e)}")
            return {"message": "An error occurred while processing your request."}, 500
