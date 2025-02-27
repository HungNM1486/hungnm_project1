from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from customer.models import CustomerProfile
from book.models import Book
from .models import Cart, CartItem
from rest_framework import viewsets, generics, permissions
from .models import Cart
from .serializers import CartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user.customerprofile)


class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return Cart.objects.get(customer=self.request.user.customerprofile)


# API: Lấy thông tin giỏ hàng
class CartAPIView(LoginRequiredMixin, APIView):
    def get(self, request):
        profile = get_object_or_404(CustomerProfile, user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=profile)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API: Thêm sách vào giỏ hàng


class AddToCartAPIView(LoginRequiredMixin, APIView):
    def post(self, request):
        book_id = request.data.get("book_id")
        quantity = request.data.get("quantity", 1)

        profile = get_object_or_404(CustomerProfile, user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=profile)
        book = get_object_or_404(Book, id=book_id)
        cart.add_item(book, quantity)
        return Response({"message": "Book added to cart"}, status=status.HTTP_200_OK)


# API: Xóa sách khỏi giỏ hàng


class RemoveFromCartAPIView(LoginRequiredMixin, APIView):
    def delete(self, request, book_id):
        profile = get_object_or_404(CustomerProfile, user=request.user)
        cart = get_object_or_404(Cart, customer=profile)
        book = get_object_or_404(Book, id=book_id)
        cart.remove_item(book)
        return Response(
            {"message": "Book removed from cart"}, status=status.HTTP_200_OK
        )


# API: Cập nhật số lượng sách


class UpdateCartAPIView(LoginRequiredMixin, APIView):
    def put(self, request, book_id):
        profile = get_object_or_404(CustomerProfile, user=request.user)
        cart = get_object_or_404(Cart, customer=profile)
        book = get_object_or_404(Book, id=book_id)
        new_quantity = request.data.get("quantity")
        if not new_quantity or int(new_quantity) <= 0:
            return Response(
                {"error": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST
            )
        cart.update_quantity(book, int(new_quantity))
        return Response({"message": "Quantity updated"}, status=status.HTTP_200_OK)


# API: Xóa toàn bộ giỏ hàng


class ClearCartAPIView(LoginRequiredMixin, APIView):
    def delete(self, request):
        profile = get_object_or_404(CustomerProfile, user=request.user)
        cart = get_object_or_404(Cart, customer=profile)
        cart.clear()
        return Response({"message": "Cart cleared"}, status=status.HTTP_200_OK)


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = CustomerProfile.objects.get(user=self.request.user)
        cart, _ = Cart.objects.get_or_create(customer=profile)
        context["cart"] = cart
        context["cart_items"] = cart.cartitem_set.all()
        context["total"] = cart.get_total()
        return context


class AddToCartView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        profile = CustomerProfile.objects.get(user=request.user)
        cart, _ = Cart.objects.get_or_create(customer=profile)
        book = get_object_or_404(Book, id=book_id)
        cart.add_item(book, quantity=1)
        return redirect("cart")


class RemoveFromCartView(LoginRequiredMixin, View):
    def get(self, request, book_id):
        profile = CustomerProfile.objects.get(user=request.user)
        cart = Cart.objects.get(customer=profile)
        book = get_object_or_404(Book, id=book_id)
        cart.remove_item(book)
        return redirect("cart")


class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, book_id):
        profile = CustomerProfile.objects.get(user=request.user)
        cart = Cart.objects.get(customer=profile)
        book = get_object_or_404(Book, id=book_id)
        new_quantity = int(request.POST.get("quantity", 1))
        cart.update_quantity(book, new_quantity)
        return redirect("cart")


class ClearCartView(LoginRequiredMixin, View):
    def get(self, request):
        profile = CustomerProfile.objects.get(user=request.user)
        cart = Cart.objects.get(customer=profile)
        cart.clear()
        return redirect("cart")
