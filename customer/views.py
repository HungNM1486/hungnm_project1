from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import CustomerProfile
from .forms import CustomerProfileForm, RegisterForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.shortcuts import render, redirect


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'customer/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = CustomerProfile.objects.get(user=self.request.user)
        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = CustomerProfile
    form_class = CustomerProfileForm
    template_name = 'customer/update_profile.html'
    success_url = reverse_lazy('customer_profile')
    
    def get_object(self):
        return CustomerProfile.objects.get(user=self.request.user)
    
class CustomLoginView(LoginView):
    template_name = 'customer/login.html'

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    
    return render(request, 'customer/register.html', {'form': form})    
