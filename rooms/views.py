from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django_countries import countries
from . import models as room_models


class HomeView(ListView):

    model = room_models.Room
    page_kwarg = "p"
    paginate_by = 10
    paginate_orphans = 5
    context_object_name = "rooms"
    template_name = "home.html"


class RoomDetailView(DetailView):

    model = room_models.Room
    template_name = "rooms/detail.html"


def search(request):
    selected_city = str.capitalize(request.GET.get("city", "Anywhere"))
    selected_country = request.GET.get("country", "KR")
    selected_room_type = int(request.GET.get("room_type", 0))

    selected = {
        "selected_city": selected_city,
        "selected_country": selected_country,
        "selected_room_type": selected_room_type,
    }

    room_types = room_models.RoomType.objects.all()

    form = {
        "countries": countries,
        "room_types": room_types,
    }

    return render(
        request,
        "rooms/search.html",
        context={**selected, **form},
    )
