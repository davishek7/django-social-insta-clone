from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post, PostImage, Comment
from .forms import PostForm, CommentForm
from .decorators import owner_required
from account.models import Profile

# Create your views here.

@login_required
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        images = request.FILES.getlist('images')
        if post_form.is_valid():
            caption = post_form.cleaned_data.get('caption')
            post = Post.objects.create(caption=caption, user=request.user)
            for image in images:
                PostImage.objects.create(image=image, post = post)
    return redirect('feed:index')

def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    images = get_list_or_404(PostImage, post=post)
    images_count = len(images)
    related_posts = Post.objects.filter(~Q(id=post.id), user=post.user).order_by('-created_at')[:6]
    title = f'{post.user.name} on Instagram: "{post.caption}"'
    context = {'post':post, 'images':images, 'images_count':images_count, 'details':True, 'related_posts':related_posts,'title':title}
    return render(request, 'post/detail.html', context=context)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect(request.META.get('HTTP_REFERER') + '#' + post.slug)

@login_required
def add_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER') + '#' + post.slug)

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
    else:
        comment.likes.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@owner_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    print(post)
    context={'post':post}
    return render(request, 'post/update.html', context=context)

@login_required
@owner_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.status = False
    post.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def add_bookmark(request, pk):
    post = get_object_or_404(Post, id=pk)
    profile = get_object_or_404(Profile, id=request.user.id)
    if post not in profile.bookmarks.all():
        profile.bookmarks.add(post)
    else:
        profile.bookmarks.remove(post)
    return redirect(request.META.get('HTTP_REFERER') + '#' + post.slug)