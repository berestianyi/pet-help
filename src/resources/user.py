from flask import render_template, make_response, request, redirect, url_for, Response
from flask_login import login_user, login_required, logout_user, current_user
from flask_restful import Resource

from src import bcrypt, db, login_manager, app
from src.utils import Validation, validate_register_form, validate_input, render_validation_response

from src.models.user import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Login(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user/login.html'), 200, headers)

    def post(self):
        errors = []
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.session.query(User).filter_by(email=email).first()

        if user:
            try:
                if bcrypt.check_password_hash(user.password, password):
                    print(f'hello {user.username}')
                    login_user(user)
                    return redirect(url_for('questionnaire'))
                else:
                    errors.append('Password is incorrect.')
            except ValueError:
                print('Invalid password hash format. Please reset your password.')
        else:
            errors.append('Email does not exist or password is incorrect.')

        return make_response(render_template('user/login.html', errors=errors), 200)


class Register(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('user/register.html'), 200, headers)

    def post(self):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        syntax_validation = validate_register_form(username, email, password, password2)

        if validate_input(syntax_validation):
            return Response(status=204)

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))


class Password(Resource):
    def get(self):
        password = request.args.get('password')

        validations = [
            Validation.length(password, 8, 32),
            Validation.one_special_character_and_english_characters(password),
        ]

        errors = validate_input(validations)
        return render_validation_response(
            errors,
            success_template='user/htmx/password/correct.html',
            error_template='user/htmx/password/errors.html',
            value=password
        )

    def post(self):
        password = request.form.get('password')
        password2 = request.form.get('password2')

        validations = [Validation.password_matching(password, password2), ]

        errors = validate_input(validations)
        return render_validation_response(
            errors,
            success_template='user/htmx/password2/correct.html',
            error_template='user/htmx/password2/errors.html',
            value=password2
        )


class Email(Resource):
    def get(self):
        email = request.args.get('email')
        validations = [Validation.email_only(email),
                       Validation.length(email, 4, 80),
                       Validation.existing_email(email),]

        errors = validate_input(validations)
        return render_validation_response(
            errors,
            success_template='user/htmx/email/correct.html',
            error_template='user/htmx/email/errors.html',
            value=email
        )


class Username(Resource):
    def get(self):
        username = request.args.get('username')
        validations = [
            Validation.english_characters_only(username),
            Validation.length(username, 4, 64),
            Validation.existing_username(username), ]

        errors = validate_input(validations)
        return render_validation_response(
            errors,
            success_template='user/htmx/username/correct.html',
            error_template='user/htmx/username/errors.html',
            value=username
        )


class FormValidation(Resource):
    def post(self):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        syntax_validation = validate_register_form(username, email, password, password2)
        errors = validate_input(syntax_validation)

        if not errors:
            return make_response(render_template("user/htmx/submit_button.html"))
        return make_response(render_template("user/htmx/button.html"))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


class Profile(Resource):
    @login_required
    def get(self):
        user = current_user
        return make_response(render_template('user/profile.html', user=user))

    @login_required
    def post(self):
        pass
