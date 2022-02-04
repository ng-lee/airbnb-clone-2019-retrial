from django.shortcuts import render
from django.core.paginator import Paginator
from . import models as room_models


def all_rooms(request):
    page = request.GET.get("p", 1)
    room_list = room_models.Room.objects.all()
    paginator = Paginator(room_list, 10)
    rooms = paginator.get_page(page)
    return render(
        request,
        "home.html",
        context={"rooms": rooms},
    )
