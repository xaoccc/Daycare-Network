from django.core.exceptions import ValidationError

def password_validator(value):
    if value.isalpha():
        raise ValidationError("Password must contain at least 1 digit")

    if value.isdigit():
        raise ValidationError("Password must contain at least 1 alphabetic character")

    if value.lower() == value:
        raise ValidationError("Password must contain at least 1 uppercase character")

    if value.upper() == value:
        raise ValidationError("Password must contain at least 1 lowercase character")

    return value

def name_validator(value):
    if not value.isalpha():
        raise ValidationError("A name can contain only alphabetic characters")

    if value[0].upper() != value[0]:
        raise ValidationError("A name should start with a capital letter")


