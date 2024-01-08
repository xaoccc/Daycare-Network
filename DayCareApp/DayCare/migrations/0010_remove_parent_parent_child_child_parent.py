# Generated by Django 4.2.8 on 2024-01-08 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DayCare', '0009_alter_location_hospitals_alter_location_schools'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parent',
            name='parent_child',
        ),
        migrations.AddField(
            model_name='child',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='DayCare.parent'),
        ),
    ]
