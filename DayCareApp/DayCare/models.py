from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from DayCareApp.DayCare.validators import password_validator
from django.contrib.auth.hashers import make_password


# Create your models here.

class Person(models.Model):
    first_name = models.CharField(max_length=40, validators=[MinLengthValidator(2, "First name should be more than two characters")])
    last_name = models.CharField(max_length=40, validators=[MinLengthValidator(2, "Last name should be more than two characters")])

    class Meta:
        abstract = True

class Location(models.Model):
    NEIGHBOURHOODS = (
        ("Borovo", "Borovo"),
        ("Belite Brezi", "Belite Brezi"),
        ("Strelbishte", "Strelbishte"),
        ("Manastirski Livadi", "Manastirski Livadi"),
        ("Luilin 1", "Luilin 1"),
        ("Luilin 2", "Luilin 2"),
        ("Luilin 3", "Luilin 3"),
        ("Luilin 4", "Luilin 4"),
        ("Luilin 5", "Luilin 5"),
        ("Luilin 6", "Luilin 6"),
        ("Luilin 7", "Luilin 7"),
        ("Luilin 8", "Luilin 8"),
        ("Luilin 9", "Luilin 9"),
        ("Mladost 1", "Mladost 1"),
        ("Mladost 2", "Mladost 2"),
        ("Mladost 3", "Mladost 3"),
        ("Mladost 4", "Mladost 4"),
        ("Nadejda 1", "Nadejda 1"),
        ("Nadejda 2", "Nadejda 2"),
        ("Ovcha kupel 1", "Ovcha kupel 1"),
        ("Ovcha kupel 2", "Ovcha kupel 2"),
    )

    location_name = models.CharField(choices=NEIGHBOURHOODS)
    hospitals = models.BooleanField()
    schools = models.BooleanField()

class Offers(Location, models.Model):
    min_rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[
        MinValueValidator(0, "Rating cannot be less than 0!"),
        MaxValueValidator(10, "Rating cannot be more than 10!")
    ])
    price_per_hour = models.DecimalField(max_digits=4, decimal_places=1, validators=[
        MinValueValidator(0, "Price cannot be less than 0!"),
        MaxValueValidator(900, "Price cannot be more than 900!")
    ])


class Child(Person):
    age = models.PositiveIntegerField(validators=[
        MaxValueValidator(18, "Maximum child age should be 18!")
    ])
    has_special_needs = models.BooleanField(default=False)

class Parent(Person):
    GENDERS = (
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    )

    age = models.PositiveIntegerField(validators=[
        MinValueValidator(18, "Parent cannot be younger than 18!"),
        MaxValueValidator(100, "Maximum age should be 100 years old!")
    ])
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0, blank=True, null=True, validators=[
        MinValueValidator(0, "Rating cannot be less than 0!"),
        MaxValueValidator(10, "Rating cannot be more than 10!")
    ])
    parent_offer = models.OneToOneField(Offers, blank=True, null=True, on_delete=models.CASCADE)
    parent_child = models.ForeignKey(Child, blank=True, null=True, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDERS)




class Profile(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(validators=[password_validator])

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(Profile, self).save(*args, **kwargs)






