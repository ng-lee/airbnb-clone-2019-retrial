import os
import requests
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.files.base import ContentFile
from django.views import View
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.views import PasswordChangeView
from . import forms, models, mixins


class LoginView(mixins.LoggedOutOnlyView, View):
    def get(self, request):
        form = forms.LoginForm()
        return render(request, "users/login.html", context={"form": form})

    def post(self, request):
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome, {user.username}")
                return redirect(reverse("core:home"))
        return render(request, "users/login.html", context={"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Good Bye")
    return redirect(reverse("core:home"))


class SignupView(mixins.LoggedOutOnlyView, FormView):

    template_name = "users/signup.html"
    success_url = reverse_lazy("core:home")
    form_class = forms.SignupForm

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, f"Welcome, {user.username}")
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["password1"].label = "Password Confirmation"
        return form


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise GithubException("Can't get token")
            else:
                token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                username = profile_json.get("login", None)
                if username is not None:
                    name = profile_json.get("name")
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        user = models.User.objects.get(username=username)
                        if user.login_method != models.User.LOGIN_GITHUB:
                            raise GithubException(
                                f"Please try with: {user.login_method}"
                            )
                    except models.User.DoesNotExist:
                        user = models.User.objects.create(
                            username=username,
                            first_name=name,
                            email=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    messages.success(request, f"Welcome, {user.username}")
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException("Can't get username from GitHub")
        else:
            raise GithubException("Can't get code for GitHub")
    except GithubException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


class KakaoException(Exception):
    pass


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException("Can't get token")
        else:
            access_token = token_json.get("access_token")
            profile_request = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            profile_json = profile_request.json()
            kakao_account = profile_json.get("kakao_account", None)
            if kakao_account is None:
                raise KakaoException("Can't get info from Kakao")
            email = kakao_account.get("email")
            profile_image = kakao_account.get("profile").get("profile_image_url")
            nickname = kakao_account.get("profile").get("nickname")
            try:
                user = models.User.objects.get(username=email)
                if user.login_method != models.User.LOGIN_KAKAO:
                    raise KakaoException(f"Please try with: {user.login_method}")
            except models.User.DoesNotExist:
                user = models.User.objects.create(
                    username=email,
                    first_name=nickname,
                    email=email,
                    login_method=models.User.LOGIN_KAKAO,
                )
                user.set_unusable_password()
                user.save()
                if profile_image is not None:
                    photo_request = requests.get(profile_image)
                    user.avatar.save(
                        f"{nickname}-avatar", ContentFile(photo_request.content)
                    )
            login(request, user)
            messages.success(request, f"Welcome, {user.username}")
            return redirect(reverse("core:home"))
    except KakaoException as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


class ProfileView(DetailView):

    model = models.User
    context_object_name = "user_obj"


class UpdateProfileView(mixins.LoggedInOnlyView, UpdateView):

    model = models.User
    template_name = "users/update-profile.html"
    fields = (
        "first_name",
        "last_name",
        "username",
        "email",
        "avatar",
        "gender",
        "bio",
        "birthdate",
        "language",
        "currency",
    )

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.user.get_absolute_url()


class UpdatePasswordView(
    mixins.EmailLoginOnlyView, mixins.LoggedInOnlyView, PasswordChangeView
):

    template_name = "users/update-password.html"

    def get_success_url(self):
        return self.request.user.get_absolute_url()
