from django.shortcuts import render
from post.models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required
def index(request):
    posts = Post.objects.select_related('user').prefetch_related('likes').filter(status=True).all()
    context = {'posts':posts}
    return render(request, 'index.html', context=context)