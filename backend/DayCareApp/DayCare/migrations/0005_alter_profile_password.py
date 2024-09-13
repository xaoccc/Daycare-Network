# Generated by Django 4.2.7 on 2023-12-01 11:41

import DayCareApp.DayCare.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DayCare', '0004_profile_is_authenticated_alter_parent_age_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='password',
            field=models.CharField(validators=[DayCareApp.DayCare.validators.password_validator]),
        ),
    ]