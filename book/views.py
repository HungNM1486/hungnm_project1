from django.views.generic import ListView, DetailView
from .models import Book
from django.shortcuts import render, redirect
from .forms import BookForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, generics
from .models import Book
from .serializers import BookSerializer

class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'book'

class APIBookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class APIBookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@login_required
def add_book(request):
    # Chỉ cho phép admin
    if not request.user.is_staff:
        return HttpResponseForbidden("Bạn không có quyền thêm sách.")

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Điều hướng đến trang danh sách sách sau khi thêm thành công
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "book/add_book.html", {"form": form})