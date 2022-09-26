from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from account.models import Profile

# Create your views here.

def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    profile = get_object_or_404(Profile, id=user.id)
    context = {'user':user, 'profile':profile}
    return render(request, 'user/profile.html', context=context)