from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from .decorators import unauthenticated_user
from django.contrib import messages

# Create your views here.

@unauthenticated_user
def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            # if get_user_model().objects.filter(email=email, is_superuser=True).exists():
            #     messages.error(request, 'You are not authorised to view this page.')
            #     return redirect(request.META.get('HTTP_REFERER'))
            # else:
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request,f'Welcome, {user.username}')
                if user.is_superuser:
                    return redirect('dashboard:home')
                else:
                    return redirect('feed:index')
    context = {'title':'Login \u2022 ', 'form':form}
    return render(request, 'auth/login.html', context=context)

@unauthenticated_user
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