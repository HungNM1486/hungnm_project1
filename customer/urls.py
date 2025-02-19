from django.urls import path
from customer.views import register_view, login_view, logout_view, profile_view, update_profile

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/update/", update_profile, name="update_profile"),
]
