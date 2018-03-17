from django import forms
from django.contrib import admin
from hotel_reservations.models import Reservation, HotelConfiguration
from datetime import timedelta


def is_valid_date_range(start, end):
    if start >= end:
        raise forms.ValidationError("Check-out date must be after check-in date")


def is_available(start, end):
    hotel_config = HotelConfiguration.get_solo()
    bookable = int(hotel_config.room_count * (hotel_config.overbooking_level + 1))
    check_date = start
    while check_date < end:
        booked = Reservation.objects.filter(check_in__lte=check_date, check_out__gt=check_date).count()
        if booked >= bookable:
            raise forms.ValidationError("There are no rooms available for the selected date range")
        check_date += timedelta(days=1)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data["check_in"]
        check_out = cleaned_data["check_out"]
        is_valid_date_range(check_in, check_out)
        is_available(check_in, check_out)
        return cleaned_data


class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm
    list_display = ['name', 'check_in', 'check_out']
