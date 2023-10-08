# Generated by Django 4.2 on 2023-10-08 21:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=255, validators=[django.core.validators.EmailValidator()]),
        ),
    ]