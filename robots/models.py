from datetime import datetime

from django.core import validators
from django.db import models


class Robot(models.Model):
    serial = models.CharField(max_length=5, blank=False, null=False, validators=[validators.RegexValidator('^..-..$')])
    model = models.CharField(max_length=2, blank=False, null=False, validators=[validators.MinLengthValidator(2)])
    version = models.CharField(max_length=2, blank=False, null=False, validators=[validators.MinLengthValidator(2)])
    created = models.DateTimeField(blank=False, null=False, validators=[validators.MaxValueValidator(datetime.now)])
