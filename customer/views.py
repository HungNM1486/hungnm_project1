from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from customer.models import CustomerProfile
from customer.forms import RegisterForm, LoginForm, CustomerProfileForm
from customer.serializers import UserSerializer, CustomerProfileSerializer

# ================= GIAO DIỆN WEB ==================

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Chuyển hướng sau khi đăng ký thành công
    else:
        form = RegisterForm()
    return render(request, "customer/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]  # Lấy tên đăng nhập từ form
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("profile")  # Chuyển hướng đến trang cá nhân
            else:
                form.add_error(None, "Tên đăng nhập hoặc mật khẩu không đúng")
    else:
        form = LoginForm()
    return render(request, "customer/login.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def profile_view(request):
    profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = CustomerProfileForm(instance=profile)
    return render(request, "customer/profile.html", {"form": form, "profile": profile})

@login_required
def update_profile(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if request.method == "POST":
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = CustomerProfileForm(instance=profile)
    return render(request, "customer/update_profile.html", {"form": form})

# ================= API (JSON) ==================

# API Đăng ký
# class APIRegisterView(generics.CreateAPIView):
#     queryset = get_user_model().objects.all()
#     serializer_class = UserSerializer
    
from rest_framework.permissions import AllowAny
    
class APIRegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # 🌟 Cho phép tất cả người dùng gọi API


# API Đăng nhập
class APILoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

# API Đăng xuất
class APILogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        request.auth.delete()  # Xóa token
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)

# API Hồ sơ cá nhân
class APIProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.customerprofile
