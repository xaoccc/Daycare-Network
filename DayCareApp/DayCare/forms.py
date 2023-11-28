from django import forms
from django.core.validators import MinLengthValidator
from DayCareApp.DayCare.validators import password_validator


class RegisterUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='Password', max_length=30, required=True, validators=[password_validator])
    first_name = forms.CharField(label="First name", max_length=40, validators=[MinLengthValidator(2)], required=True)
    last_name = forms.CharField(label="Last name", max_length=40, validators=[MinLengthValidator(2)], required=True)



