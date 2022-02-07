from django.shortcuts import render
from django.views import View
from users.forms import LoginForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "users/login.html", context={"form": form})

    def post(self, request):
        pass
