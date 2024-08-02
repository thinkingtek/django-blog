from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('posts/', PostList.as_view(), name='posts'),
    path('favourite-posts/', UsersFav.as_view(), name='fovourite-posts'),
    path('create-post/', PostCreate.as_view(), name='create-post'),
    path('categories/', Categories.as_view(), name='all-categories'),
    path('search-posts/', PostSearch.as_view(), name='search-posts'),
    path('post/<slug:slug>/update/', PostUpdate.as_view(), name='post-update'),
    path('post/<slug:slug>/comments/',
         PostComments.as_view(), name='post-comments'),
    path('post/<slug:slug>/delete/', deletePost, name='post-delete'),
    path('delete-comment/<int:pk>/<slug:slug>/',
         delete_comment, name='comment-delete'),
    path('category-posts/<str:name>',
         CategoryPostList.as_view(), name='category-posts'),
    path('author-posts/<str:username>',
         UserPostList.as_view(), name='user-posts'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post-details'),
    path('post-comment/<slug:slug>/', redirectComment, name='redirect-comment'),

    path('post-comment-page/<slug:slug>/',
         redirectCommentPage, name='redirect-comment-page'),
    path('like-post/<slug:slug>/', like, name='like-post'),
    path('favourite-post/<slug:slug>/', addFavourite, name='favourite-post'),
]
