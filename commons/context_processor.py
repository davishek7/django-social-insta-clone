from post.forms import PostForm, PostImageForm, CommentForm
from account.models import Profile
from django.shortcuts import get_object_or_404

def common_context(request):
    return {
        'post_form' : PostForm(),
        'image_form' : PostImageForm(),
        'comment_form' : CommentForm(),
        'profile' : get_object_or_404(Profile, id=request.user.id) if request.user.is_authenticated else None
    }