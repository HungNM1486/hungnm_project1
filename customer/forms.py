from django import forms
from django.contrib.auth import get_user_model
from customer.models import CustomerProfile

User = get_user_model()

class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Xác nhận mật khẩu")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Mật khẩu không khớp.")
        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email này đã được sử dụng.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            CustomerProfile.objects.create(user=user)
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label="Tên đăng nhập")
    password = forms.CharField(widget=forms.PasswordInput)



class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['phone_number', 'address']
