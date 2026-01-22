from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Products

# نموذج التسجيل
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username'] # كلمة المرور تضاف تلقائياً من UserCreationForm

# نموذج تسجيل الدخول
class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

# نموذج المنتجات (هنا التعديل المهم)
class ProductForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = '__all__'  # يجب أن تكون محاطة بشرطتين سفليتين من الجهتين لتعمل