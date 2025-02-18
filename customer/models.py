from django.db import models
from django.contrib.auth.models import User

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_profile(self, data):
        for field, value in data.items():
            setattr(self, field, value)
        self.save()

    def get_profile(self):
        return {
            'username': self.user.username,
            'email': self.user.email,
            'phone_number': self.phone_number,
            'address': self.address,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def __str__(self):
        return self.user.username
