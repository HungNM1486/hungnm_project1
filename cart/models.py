from django.db import models
from customer.models import CustomerProfile
from book.models import Book
from decimal import Decimal
from bson.decimal128 import Decimal128  # Import Decimal128 từ MongoDB

class Cart(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_item(self, book, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(cart=self, book=book)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

    def remove_item(self, book):
        CartItem.objects.filter(cart=self, book=book).delete()

    def update_quantity(self, book, quantity):
        try:
            cart_item = CartItem.objects.get(cart=self, book=book)
            cart_item.quantity = quantity
            cart_item.save()
        except CartItem.DoesNotExist:
            pass

    def get_total(self):
        return sum(item.quantity * item.book.price for item in self.cartitem_set.all())

    def clear(self):
        self.cartitem_set.all().delete()

    def __str__(self):
        return f"Cart của {self.customer.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.book.title}"
