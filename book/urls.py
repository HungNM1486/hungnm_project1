from django.urls import path
from .views import add_book, BookListView, BookDetailView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('add/', add_book, name='add_book'),
]
