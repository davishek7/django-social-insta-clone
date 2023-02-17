from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from post.models import Post

# Create your views here.

def search(request):

    search_term = request.GET.get('q')

    users = get_user_model().objects.filter(~Q(id=request.user.id)).filter(Q(username__icontains=search_term) | Q(name__icontains=search_term)).filter(is_active=True).all()

    posts = Post.objects.filter(status=True).filter(caption__icontains=search_term).all()

    context = {'search_term':search_term, 'users':users, 'posts':posts}

    return render(request, 'search/search-results.html', context=context)