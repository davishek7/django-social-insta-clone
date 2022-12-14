from django.shortcuts import render
from django.db.models import Q
from post.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


@login_required
def index(request):
    posts = Post.objects.select_related('user').prefetch_related('likes').filter(status=True).filter(
        Q(user_id__in=request.user.profile.followings.all()) | Q(user=request.user)).all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts': page_obj}
    return render(request, 'index.html', context=context)
