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
    city = request.GET.get("city", "Anywhere")
    city = str.capitalize(city)
    room_types = room_models.RoomType.objects.all()
    return render(
        request,
        "rooms/search.html",
        context={"city": city, "countries": countries, "room_types": room_types},
    )
