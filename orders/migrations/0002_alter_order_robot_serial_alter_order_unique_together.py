# Generated by Django 4.2 on 2023-10-09 14:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0002_alter_customer_email'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='robot_serial',
            field=models.CharField(max_length=5, validators=[django.core.validators.RegexValidator('^..-..$')]),
        ),
        migrations.AlterUniqueTogether(
            name='order',
            unique_together={('customer', 'robot_serial')},
        ),
    ]
