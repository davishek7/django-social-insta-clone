from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Post, PostImage, Comment, Reply
from .forms import PostForm, CommentForm, ReplyForm
from .decorators import post_user_required, comment_user_required, reply_user_required
from account.models import Profile
from django.contrib.auth import get_user_model
from django.contrib import messages
from story.models import Story
from commons.decorators import normal_user_only

# Create your views here.

@login_required
@normal_user_only
def create_post(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        images = request.FILES.getlist('images')
        if post_form.is_valid():
            caption = post_form.cleaned_data.get('caption')
            post = Post.objects.create(caption=caption, user=request.user)
            for image in images:
                PostImage.objects.create(image=image, post = post)
                if request.POST.get('addToStory'):
                    Story.objects.create(caption=caption, user=request.user, image=image)
    return redirect('feed:index')

def post_details(request, slug):
    post = get_object_or_404(Post, slug=slug)
    images = get_list_or_404(PostImage, post=post)
    images_count = len(images)
    related_posts = Post.objects.filter(~Q(id=post.id), user=post.user, status=True).order_by('-created_at')[:6]
    title = f'{post.user.name} on Instagram: "{post.caption}"'
    context = {'post':post, 'images':images, 'images_count':images_count, 'details':True, 'related_posts':related_posts,'title':title}
    return render(request, 'post/detail.html', context=context)

def get_post_comments(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {'post':post}
    return render(request, 'post/post_comments.html', context=context)

@login_required
@normal_user_only
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
@normal_user_only
@comment_user_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    comment.status = False
    comment.save(update_fields=['status'])
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
def add_like(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.user not in post.likes.all():
        post.likes.add(request.user)
    else:
        post.likes.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER') + '#' + post.slug)

@login_required
@normal_user_only
def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.user not in comment.likes.all():
        comment.likes.add(request.user)
    else:
        comment.likes.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
@post_user_required
def update_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        print(request.FILES)
        caption = request.POST.get('caption')
        if caption != post.caption:
            post.caption = caption
            post.save()
        new_images = request.FILES.getlist('new_images')
        for image in new_images:
            PostImage.objects.create(image=image, post=post)
        delete_images = request.POST.getlist('delete_images')
        PostImage.objects.filter(id__in=delete_images, post=post).delete()
        messages.success(request, 'Post updated successfully!')
        return redirect('post:post_details', slug=post.slug)
    context={'post':post}
    return render(request, 'post/update.html', context=context)

@login_required
@normal_user_only
@post_user_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.status = False
    post.save()
    return redirect('/')

@login_required
@normal_user_only
def add_bookmark(request, pk):
    post = get_object_or_404(Post, id=pk)
    profile = get_object_or_404(Profile, id=request.user.id)
    if post not in profile.bookmarks.all():
        profile.bookmarks.add(post)
        messages.info(request, f'{post.caption} saved to your collection.')
    else:
        profile.bookmarks.remove(post)
        messages.warning(request, f'{post.caption} removed from your collection.')
    return redirect(request.META.get('HTTP_REFERER') + '#' + post.slug)

@login_required
@normal_user_only
def add_favorites(request, user_id):
    post_user = get_object_or_404(get_user_model(), id=user_id)
    profile = get_object_or_404(Profile, id=request.user.id)
    if post_user not in profile.favourites.all():
        profile.favourites.add(post_user)
        messages.info(request, f'{post_user.username} added to your favorites.')
    else:
        profile.favourites.remove(post_user)
        messages.warning(request, f'{post_user.username} removed from your favourites.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
def explore(request):
    posts = Post.objects.select_related('user').prefetch_related('likes').exclude(user = request.user).filter(
        status=True).filter(~Q(user__id__in=request.user.profile.followings.all()) | ~Q(id__in=request.user.post_likes.all())).order_by('?').all()
    
    context = {'posts':posts}
    return render(request, 'post/explore.html', context=context)

@login_required
@normal_user_only
def add_reply(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.method == 'POST':
        reply_id = request.POST.get('reply')
        reply_form = ReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = request.user
            reply.comment = comment
            if reply_id:
                replied_reply = get_object_or_404(Reply, id=reply_id)
                reply.reply = replied_reply
            reply.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
@reply_user_required
def delete_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk)
    reply.status = False
    reply.save(update_fields=['status'])
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
def like_reply(request, pk):
    reply = get_object_or_404(Reply, id=pk)
    if request.user not in reply.likes.all():
        reply.likes.add(request.user)
    else:
        reply.likes.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))