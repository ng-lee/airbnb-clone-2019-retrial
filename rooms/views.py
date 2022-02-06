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
    selected_price = int(request.GET.get("price", 0))
    selected_guests = int(request.GET.get("guests", 0))
    selected_beds = int(request.GET.get("beds", 0))
    selected_bedrooms = int(request.GET.get("bedrooms", 0))
    selected_baths = int(request.GET.get("baths", 0))
    selected_instant_book = request.GET.get("instant_book", False)
    selected_super_host = request.GET.get("super_host", False)
    selected_amenities = request.GET.getlist("amenities")
    selected_facilities = request.GET.getlist("facilities")

    selected = {
        "selected_city": selected_city,
        "selected_country": selected_country,
        "selected_room_type": selected_room_type,
        "selected_price": selected_price,
        "selected_guests": selected_guests,
        "selected_beds": selected_beds,
        "selected_bedrooms": selected_bedrooms,
        "selected_baths": selected_baths,
        "selected_amenities": selected_amenities,
        "selected_facilities": selected_facilities,
        "selected_instant_book": selected_instant_book,
        "selected_super_host": selected_super_host,
    }

    room_types = room_models.RoomType.objects.all()
    amenities = room_models.Amenity.objects.all()
    facilities = room_models.Facility.objects.all()

    form = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if selected_city != "Anywhere":
        filter_args["city__contains"] = selected_city

    filter_args["country"] = selected_country

    if selected_room_type != 0:
        filter_args["room_type__pk"] = selected_room_type

    rooms = room_models.Room.objects.filter(**filter_args)

    return render(
        request,
        "rooms/search.html",
        context={**selected, **form, "rooms": rooms},
    )
