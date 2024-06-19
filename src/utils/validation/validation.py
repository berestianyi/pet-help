import re
from typing import Tuple

from flask import render_template, make_response

from src.models.user import User


class Validation:
    @staticmethod
    def length(value, min_value, max_value) -> str | None:
        if len(value) < min_value:
            return f"Value must be greater than or equal to {min_value}"
        if len(value) > max_value:
            return f"Value must be less than or equal to {max_value}"

    @staticmethod
    def english_characters_only(value) -> str | None:
        if not re.match(r'^[A-Za-z0-9]*$', value):
            return 'Field must contain only English characters and numbers.'
        return None

    @staticmethod
    def at_least_one_special_character(value) -> str | None:
        if not re.match(r'^(?=.*[!@#$%^&*()_+]).*$', value):
            return 'Password must contain at least one special character (!@#$%^&*()_+).'
        return None

    @staticmethod
    def one_special_character_and_english_characters(value) -> str | None:
        if not re.match(r'^[A-Za-z0-9!@#$%^&*()_+]*$', value):
            return 'Field must contain only English characters, numbers, and special characters (!@#$%^&*()_+).'
        return None

    @staticmethod
    def email_only(value) -> str | None:
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            return 'Invalid email address.'
        return None

    @staticmethod
    def password_matching(password, password2) -> str | None:
        if password != password2:
            return 'Password must match.'
        return None

    @staticmethod
    def existing_username(username) -> str | None:
        existing_user_username = User.query.filter_by(username=username).first()
        if existing_user_username:
            return 'This username already exists.'

    @staticmethod
    def existing_email(email) -> str | None:
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_email:
            return 'This email address already exists.'

    @staticmethod
    def date_format(value) -> str | None:
        if not re.match(r'^(0[1-9]|1[0-2])/(0[1-9]|[12][0-9]|3[01])/([0-9]{4})$', value):
            return 'Date is not valid'
        else:
            return None

    @staticmethod
    def at_least_3_chars(value) -> str | None:
        if len(value) < 3:
            return 'Field is too short'
        else:
            return None

    @staticmethod
    def correct_phone_number(value) -> str | None:
        if not re.match(r'\(\d{3}\) \d{3}-\d{4}', value):
            return 'Phone number is invalid.'
        else:
            return None


def validate_input(validations):
    errors = [error for error in validations if error is not None]
    return errors


def render_validation_response(errors, error_template: str, success_template: str, value: str):
    if errors:
        return make_response(render_template(error_template, errors=errors, value=value), 200)
    return make_response(render_template(success_template, value=value), 200)


def validate_register_form(username, email, password, password2):
    return [
        Validation.length(username, 4, 64),
        Validation.english_characters_only(username),
        Validation.length(password, 8, 32),
        Validation.one_special_character_and_english_characters(password),
        Validation.password_matching(password, password2),
        Validation.length(email, 4, 80),
        Validation.email_only(email),
        Validation.existing_username(username),
        Validation.existing_email(email),
    ]