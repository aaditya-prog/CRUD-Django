from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("changepass/", views.user_change_pass, name="changepass"),
    path("profile/", views.profile, name="profile"),
    path(
        "activate-user/<uidb64>/<token>",
        views.activate_user,
        name="activate",
    ),
]
