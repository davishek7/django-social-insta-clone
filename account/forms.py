from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control mb-2 rounded', 'placeholder':'Email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control mb-2 rounded', 'placeholder':'Username'}))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control mb-2 rounded', 'placeholder':'Full Name'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control mb-2 rounded', 'placeholder':'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control mb-3 rounded', 'placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ['email', 'username', 'name', 'password1', 'password2']


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control mb-2 rounded', 'placeholder':'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class':'form-control mb-3 rounded', 'placeholder':'Password'}))

    class Meta:
        fields = ['email', 'password']