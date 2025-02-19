from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from customer.models import CustomerProfile
from customer.forms import RegisterForm, LoginForm, CustomerProfileForm

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
    # Sử dụng get_or_create để lấy CustomerProfile, nếu chưa có thì tạo mới
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
            return redirect("profile")  # Chuyển hướng về trang hồ sơ cá nhân sau cập nhật
    else:
        form = CustomerProfileForm(instance=profile)
    return render(request, "customer/update_profile.html", {"form": form})
