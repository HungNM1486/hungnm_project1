from django.urls import path
from .views import add_book, BookListView, BookDetailView, APIBookListView, APIBookDetailView


urlpatterns = [
    # Giao diện web (HTML)
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('add/', add_book, name='add_book'),

    # API REST (JSON)
    path('api/', APIBookListView.as_view(), name='api_book_list'),
    path('api/<int:pk>/', APIBookDetailView.as_view(), name='api_book_detail'),
]