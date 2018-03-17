from django.db import models
from solo.models import SingletonModel
from django.core.exceptions import ValidationError
import re


def is_positive(num):
    if num <= 0:
        raise ValidationError("Value must be greater than 0")


def is_not_negative(num):
    if num < 0:
        raise ValidationError("Value must be greater than or equal to 0")


def is_email_address(email):
    email_pattern = r"^\w+@\w+\.\w+$"
    regex = re.compile(email_pattern)
    if regex.match(email) is None:
        raise ValidationError("Value must be an email address")


class HotelConfiguration(SingletonModel):
    room_count = models.IntegerField(validators=[is_positive], default=100)
    overbooking_level = models.FloatField(validators=[is_not_negative], default=0)


class Reservation(models.Model):
    id = models.AutoField()
    id.primary_key = True
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, validators=[is_email_address])
    check_in = models.DateField()
    check_out = models.DateField()
