from django import forms
from django.forms.widgets import PasswordInput
from django.core.validators import MinLengthValidator, MinValueValidator
from DayCareApp.DayCare.validators import password_validator, name_validator


class RegisterUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=30, required=True)
    password = forms.CharField(label='Password', max_length=30, required=True, widget=PasswordInput(), validators=[MinLengthValidator(8,  "Password must be at least 8 characters long!"), password_validator])
    password_repeat = forms.CharField(label='Confirm password', max_length=30, required=True, widget=PasswordInput(), validators=[MinLengthValidator(8,  "Password must be at least 8 characters long!"), password_validator])
    first_name = forms.CharField(label="First name", max_length=40, validators=[MinLengthValidator(2), name_validator], required=True)
    last_name = forms.CharField(label="Last name", max_length=40, validators=[MinLengthValidator(2), name_validator], required=True)
    age = forms.IntegerField(label="Age", max_value=100, validators=[MinValueValidator(18, "Parent cannot be younger than 18!")])
    CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    ]

    gender = forms.ChoiceField(label="Gender", choices=CHOICES)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("password_repeat")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    password = forms.CharField(label='Password', required=True, widget=PasswordInput())

class UsernameEditForm(forms.Form):
    username = forms.CharField(label='Enter new username:', required=True)






