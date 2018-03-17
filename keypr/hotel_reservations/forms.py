from django import forms
from django.contrib import admin
from hotel_reservations.models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"


class ReservationAdmin(admin.ModelAdmin):
    form = ReservationForm
    list_display = ['name', 'check_in', 'check_out']
