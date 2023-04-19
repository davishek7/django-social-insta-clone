from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from post.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from commons.decorators import normal_user_only

# Create your views here.

@login_required
@normal_user_only
def search(request):

    search_term = request.GET.get('q').strip()

    if search_term == "":
        messages.error(request, 'Please enter a search term!')
        return redirect(request.META.get('HTTP_REFERER'))
            
    users = get_user_model().objects.exclude(Q(id=request.user.id)|Q(is_superuser=True)).filter(Q(username__icontains=search_term) | Q(name__icontains=search_term)).filter(is_active=True).all()

    posts = Post.objects.filter(status=True).filter(caption__icontains=search_term).order_by('?').all()

    context = {'search_term':search_term, 'users':users, 'posts':posts}

    return render(request, 'search/search-results.html', context=context)