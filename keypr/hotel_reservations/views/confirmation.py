from django.views.generic.base import View
from django.shortcuts import render


class Confirmation(View):

    def get(self, request, *args):
        return render(request, "confirmation.html", {})
