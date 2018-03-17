from django.views.generic.base import View
from django.shortcuts import render
from hotel_reservations.forms import ReservationForm
from hotel_reservations.models import Reservation
from django.http import HttpResponseRedirect


class NewReservation(View):

    def get(self, request, *args):
        context = {}
        form = ReservationForm()
        context["form"] = form
        return render(request, "index.html", context)

    def post(self, request, *args):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = Reservation(name=form.cleaned_data["name"],
                                      email=form.cleaned_data["email"],
                                      check_in=form.cleaned_data.get("check_in"),
                                      check_out=form.cleaned_data["check_out"])
            reservation.save()
            return HttpResponseRedirect("/confirmation/")
        else:
            context = {"form": form}
            return render(request, "index.html", context)