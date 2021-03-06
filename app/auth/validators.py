"""Validators to be used in WTForms for the auth application.
    Validator names are written to be conformant with existing `wtforms.valiator.ValidatorFunctions`.

    TODO: Convert these to classes so we can use `.message` or something in the tests.
"""
import re

from wtforms.validators import Email, ValidationError, StopValidation

from app.auth.models import User


def NoSpecialChars():
    """Validator to make sure special characters or spaces aren't in the supplied field's data."""

    def _(form, field):
        if not re.match(r'^\w+$', field.data):
            raise StopValidation(
                'Must be letters (uppercase or lowercase), digits, and underscores only.')

    return _


def Unique():
    """Validator to make sure the field doesn't already exist in the DB (is unique)."""

    def _(form, field):
        field_model_column = getattr(User.__table__.columns, field.name)
        if User.query.filter(
                field_model_column == field.data).scalar() is not None:
            raise StopValidation('{} must be unique.'.format(field.label.text))

    return _


def EmailIsValid():
    """Validator to make sure email is valid.
        This is a wrapper around `wtforms.validators.Email()`, but it raises a StopValidation exception.
    """

    def _(form, field):
        try:
            Email()(form, field)
        except ValidationError:
            raise StopValidation('Email must be valid.')

    return _
