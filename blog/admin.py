from django.contrib import admin
from .models import Post, Category, Comment, PostView
from django import forms

admin.site.register(Category)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'edictors_pick', 'image', 'categories',
                  'title', 'slug', 'content', 'likes', 'favourites')
        widgets = {'categories': forms.CheckboxSelectMultiple}

    def clean_categories(self):
        categories = self.cleaned_data.get("categories")
        if categories.count() > 2:
            raise forms.ValidationError(
                "You can only select two categories for a post")
        return categories


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostForm
    # search_fields = ('title', 'author_name')
    list_filter = ('publish', 'edictors_pick',
                   'date_posted', 'date_updated')
    list_display = ('title', 'author', 'publish',
                    'edictors_pick', 'date_posted')
    prepopulated_fields = {"slug": ('title',)}


# @admin.register(PostView)
# class ViewAdmin(admin.ModelAdmin):
#     search_fields = ('post',)
#     list_filter = ('timestamp', 'post')
#     list_display = ('user', 'post', 'timestamp')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('post',)
    # list_filter = ('timestamp', 'post')
    list_display = ('user', 'post', 'show', 'timestamp',)
