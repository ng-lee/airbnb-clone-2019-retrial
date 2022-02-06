from django.shortcuts import render
from django.views.generic import ListView, DetailView
from . import models as room_models, forms


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

    form = forms.SearchForm()

    return render(request, "rooms/search.html", context={"form": form})
