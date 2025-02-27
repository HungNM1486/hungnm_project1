from django.urls import path
from customer.views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    update_profile,
    APIRegisterView,
    APILoginView,
    APILogoutView,
    APIProfileView,
)

urlpatterns = [
    # Giao diện web
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("profile/update/", update_profile, name="update_profile"),
    # API JSON
    path("api/register/", APIRegisterView.as_view(), name="api_register"),
    path("api/login/", APILoginView.as_view(), name="api_login"),
    path("api/logout/", APILogoutView.as_view(), name="api_logout"),
    path("api/profile/", APIProfileView.as_view(), name="api_profile"),
]
