from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/books/')),  # Chuyển hướng đường dẫn trống đến /books/
    path('books/', include('book.urls')),
    path('customer/', include('customer.urls')),
    path('cart/', include('cart.urls')),
]
