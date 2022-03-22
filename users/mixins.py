from django.shortcuts import redirect, reverse
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy


class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        return reverse("core:home")


class LoggedOutOnlyView(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect(reverse("core:home"))


class LoggedInOnlyView(LoginRequiredMixin):

    login_url = reverse_lazy("users:login")
