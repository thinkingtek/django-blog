from django import forms
from .models import Post, Category, Comment
from django.db.models import Q
from .models import Post


class SearchForm(forms.Form):
    search = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Search Posts'}))

    class Meta:
        fields = "__all__"


class CustomC(forms.ModelMultipleChoiceField):
    def label_from_instance(self, categories):
        return "%s" % categories.name


class PostForm(forms.ModelForm):
    categories = CustomC(queryset=Category.objects.all(),
                         widget=forms.CheckboxSelectMultiple(attrs={
                             'class': 'checkme',
                             'onclick': 'return validateCheck();',
                         }))

    # content = forms.CharField(
    #     widget=TinyMCEWidget(
    #         mce_attrs={'required': False, 'cols': 30, 'rows': 10}
    #     )
    # )

    class Meta:
        model = Post
        fields = ('image', 'categories', 'title', 'slug', 'content')

    def clean_categories(self):
        categories = self.cleaned_data.get("categories")
        if categories.count() > 2:
            raise forms.ValidationError(
                "You can only select two categories for a post")
        return categories


class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, label='Content', widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'rows': 4,
    }))

    class Meta:
        model = Comment
        fields = ['content']
