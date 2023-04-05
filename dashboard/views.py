from django.shortcuts import render
from django.contrib.auth import get_user_model
from post.models import Post
from django_hosts.resolvers import reverse

# Create your views here.

def home(request):

    users = get_user_model().objects.exclude(is_superuser = True).all()[:10]
    posts = Post.objects.select_related('user').prefetch_related('likes').filter(status=True).all()

    context = {'users':users, 'posts':posts}
    return render(request, 'dashboard/index.html', context=context)