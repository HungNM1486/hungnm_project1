from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from customer.models import CustomerProfile
from book.models import Book
from .models import Cart, CartItem

class CartView(LoginRequiredMixin, TemplateView):
    template_name = 'cart/cart.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = CustomerProfile.objects.get(user=self.request.user)
        cart, _ = Cart.objects.get_or_create(customer=profile)
        context['cart'] = cart
        context['cart_items'] = cart.cartitem_set.all()
        context['total'] = cart.get_total()
        return context

class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        profile = CustomerProfile.objects.get(user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=profile)
        book = get_object_or_404(Book, id=book_id)
        cart.add_item(book, quantity=1)
        return redirect('cart')

class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        profile = CustomerProfile.objects.get(user=request.user)
        cart = Cart.objects.get(customer=profile)
        book = get_object_or_404(Book, id=book_id)
        cart.remove_item(book)
        return redirect('cart')

class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        profile = CustomerProfile.objects.get(user=request.user)
        cart = Cart.objects.get(customer=profile)
        book = get_object_or_404(Book, id=book_id)
        new_quantity = int(request.POST.get('quantity', 1))
        cart.update_quantity(book, new_quantity)
        return redirect('cart')

class ClearCartView(LoginRequiredMixin, View):
    def get(self, request):
        profile = CustomerProfile.objects.get(user=request.user)
        cart = Cart.objects.get(customer=profile)
        cart.clear()
        return redirect('cart')
