from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm

# Create your views here.

def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('feed:index')
    context = {'title':'Login \u2022 ', 'form':form}
    return render(request, 'auth/login.html', context=context)

def signup(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    context = {'title':'Sign up \u2022 ', 'form':form}
    return render(request, 'auth/register.html', context=context)

@login_required
def logout_user(request):
    logout(request)
    return redirect('account:login')