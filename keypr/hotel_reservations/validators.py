import re
from django.core.exceptions import ValidationError
from datetime import timedelta
import datetime


def is_positive(num):
    if num <= 0:
        raise ValidationError("Value must be greater than 0")


def is_not_negative(num):
    if num < 0:
        raise ValidationError("Value must be greater than or equal to 0")


def is_email_address(email):
    email_pattern = r"^[^\s@]+@[\w\.\-]+\.[\w\.\-]+$"
    regex = re.compile(email_pattern)
    if regex.match(email) is None:
        raise ValidationError("Value must be an email address")


def is_future_date(date):
    today = datetime.date.today()
    if today > date:
        raise ValidationError("Provided date must not be in the past")


def is_valid_date_range(start, end):
    if start >= end:
        raise ValidationError("Check-out date must be after check-in date")


def is_available(start, end):
    from hotel_reservations.models import Reservation, HotelConfiguration

    hotel_config = HotelConfiguration.get_solo()
    bookable = int(hotel_config.room_count * (hotel_config.overbooking_level + 1))
    reservations = Reservation.objects.filter(check_in__lt=end, check_out__gt=start)
    check_date = start
    while check_date < end:
        booked = len([r for r in reservations if r.includes_date(check_date)])
        if booked >= bookable:
            raise ValidationError("There are no rooms available for the selected date range")
        check_date += timedelta(days=1)
