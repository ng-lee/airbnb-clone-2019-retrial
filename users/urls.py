from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/github", views.github_login, name="github-login"),
    path("login/github/callback", views.github_callback, name="github-callback"),
    path("login/kakao", views.kakao_login, name="kakao-login"),
    path("login/kakao/callback", views.kakao_callback, name="kakao-callback"),
    path("logout/", views.logout_view, name="logout"),
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("<int:pk>/", views.ProfileView.as_view(), name="profile"),
    path("update-profile/", views.UpdateProfileView.as_view(), name="update-profile"),
    path(
        "update-password/", views.UpdatePasswordView.as_view(), name="update-password"
    ),
]
