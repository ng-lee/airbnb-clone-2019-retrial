from django import forms
from rooms import models as room_models


class SearchForm(forms.Form):

    city = forms.CharField()
    price = forms.IntegerField()
    room_type = forms.ModelChoiceField(queryset=room_models.RoomType.objects.all())
