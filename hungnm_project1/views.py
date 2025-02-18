# ecommerce_project/views.py (ví dụ)
from django.http import HttpResponse

def home(request):
    return HttpResponse("Chào mừng đến với E-commerce Website!")
