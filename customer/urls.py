from django.urls import path
from .views import ProfileView, UpdateProfileView, CustomLoginView, register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='customer_profile'),
    path('profile/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
