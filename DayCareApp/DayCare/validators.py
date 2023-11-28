from django.core.exceptions import ValidationError

def password_validator(value):
    if value.isalpha():
        raise ValidationError("Password must contain at least 1 digit")

    elif value.isdigit():
        raise ValidationError("Password must contain at least 1 alphabetic character")

    elif value.lower() == value:
        raise ValidationError("Password must contain at least 1 uppercase character")

    elif len(value) < 8:
        raise ValidationError("Password must be at least 8 characters long")

    return value
