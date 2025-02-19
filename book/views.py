from django.views.generic import ListView, DetailView
from .models import Book
from django.shortcuts import render, redirect
from .forms import BookForm
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required

class BookListView(ListView):
    model = Book
    template_name = 'book/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'book/book_detail.html'
    context_object_name = 'book'


@login_required
def add_book(request):
    # Chỉ cho phép admin (hoặc staff) thêm sách
    if not request.user.is_staff:
        # Bạn có thể chuyển hướng đến trang khác hoặc trả về thông báo lỗi
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