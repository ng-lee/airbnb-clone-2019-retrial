from django.views.generic import ListView
from django.shortcuts import render
from . import models as room_models


class HomeView(ListView):

    model = room_models.Room
    page_kwarg = "p"
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"
    template_name = "home.html"


def room_detail(request, pk):

    return render(request, "rooms/room_detail.html")
