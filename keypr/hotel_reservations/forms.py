from django import forms
from django.contrib import admin
from hotel_reservations.models import Reservation
from hotel_reservations.validators import is_valid_date_range, is_available

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"


class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm
    list_display = ['name', 'check_in', 'check_out']
