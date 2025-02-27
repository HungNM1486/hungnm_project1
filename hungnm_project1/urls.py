from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "", RedirectView.as_view(url="/books/")
    ),  # Chuyển hướng đường dẫn trống đến /books/
    path("books/", include("book.urls")),
    path("customer/", include("customer.urls")),
    path("cart/", include("cart.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
