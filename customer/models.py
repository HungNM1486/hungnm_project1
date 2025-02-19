from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):  
    email = models.EmailField(unique=True)  # Vẫn giữ email là duy nhất
    is_verified = models.BooleanField(default=False)  # Xác thực email  

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    # Thay đổi ở đây:
    USERNAME_FIELD = 'username'   # Sử dụng tên đăng nhập làm trường chính
    REQUIRED_FIELDS = ['email']   # Email trở thành trường bắt buộc (không dùng làm username)

    def __str__(self):
        return self.username

class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def update_profile(self, data):
        allowed_fields = ['phone_number', 'address']
        for field, value in data.items():
            if field in allowed_fields:
                setattr(self, field, value)
        self.save()

    def get_profile(self):
        return {
            'username': self.user.username,
            'email': self.user.email,
            'is_verified': self.user.is_verified,
            'phone_number': self.phone_number,
            'address': self.address,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }

    def __str__(self):
        return self.user.email
