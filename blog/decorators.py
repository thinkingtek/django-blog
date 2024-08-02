from django.shortcuts import redirect, get_object_or_404
from .models import Post, Comment


def author_check(view_func):
    def wrapper_func(request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs.get('slug'))
        if request.user == post.author:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('blog:index')

    return wrapper_func


def comment_user_check(view_func):
    def wrapper_func(request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('pk'))
        if request.user == comment.user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('blog:index')

    return wrapper_func
