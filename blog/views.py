from .imports.views_imports import *


def category_list(request):
    form = SearchForm(request.GET or None)
    categories = Post.objects.filter(publish=True).values(
        'categories__name').annotate(Count('categories__name'))[:5]
    all_categories = Post.objects.filter(publish=True).values(
        'categories__name').annotate(Count('categories__name'))
    return {'categories': categories, 'all_categories': all_categories, 'search_form': form}


@login_required
def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('blog:post-details', slug=slug)


@login_required
def addFavourite(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user in post.favourites.all():
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return redirect('blog:post-details', slug=slug)


@login_required
@author_check
def deletePost(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.delete()
    return redirect('blog:posts')


@login_required
@comment_user_check
def delete_comment(request, pk, slug):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect(reverse("blog:post-details", kwargs={'slug': post.slug}))


@login_required
def redirectComment(request, slug):
    return redirect('blog:post-details', slug=slug)


@login_required
def redirectCommentPage(request, slug):
    return redirect('blog:post-comments', slug=slug)


class Index(TemplateView):
    template_name = 'blog/index.html'

    def get_context_data(self, **kwargs):
        latest_posts = Post.objects.filter(publish=True)[:4]
        trending_posts = Post.objects.filter(publish=True)
        editors_first = Post.objects.filter(edictors_pick=True).first
        editors_pick = Post.objects.filter(edictors_pick=True)[1:3]
        context = super().get_context_data(**kwargs)
        context['title'] = 'Hompage'
        context['editors_first'] = editors_first
        context['editors_pick'] = editors_pick
        context['trending_posts'] = trending_posts
        context['latest_posts'] = latest_posts
        context["home_active"] = True
        return context


class PostList(ListView):
    queryset = Post.objects.filter(publish=True).order_by('-date_posted')
    context_object_name = 'posts'
    paginate_by = 8
    template_name = 'blog/posts.html'

    def get_queryset(self):
        posts = Post.objects.filter(publish=True).order_by('-date_posted')
        category = self.request.GET.get('category', None)
        if category:
            posts = posts.filter(categories__name=category)
        return posts

    def get_context_data(self, **kwargs):
        category_name = self.request.GET.get('category', None)
        context = super().get_context_data(**kwargs)
        context["post_active"] = True
        context["nav_active"] = True
        context["view_name"] = 'Latest Posts'
        context["category_name"] = category_name
        return context


class UserPostList(ListView):
    context_object_name = 'posts'
    paginate_by = 8
    template_name = 'blog/user-posts.html'

    def get_queryset(self):
        user = get_object_or_404(
            User, username=self.kwargs.get('username'))
        return Post.objects.filter(publish=True, author=user)

    def get_context_data(self, **kwargs):
        user = get_object_or_404(
            User, username=self.kwargs.get('username'))
        context = super().get_context_data(**kwargs)
        context["post_active"] = True
        context["view_name"] = f"{user} Posts"
        return context


class Categories(ListView):
    template_name = 'blog/categories.html'
    context_object_name = 'all_categories'
    queryset = Post.objects.filter(publish=True).values(
        'categories__name').annotate(Count('categories__name'))

    def get_context_data(self, **kwargs):
        latest_posts = Post.objects.filter(publish=True)[:4]
        trending_posts = Post.objects.filter(publish=True)
        editors_first = Post.objects.filter(edictors_pick=True).first
        editors_pick = Post.objects.filter(edictors_pick=True)[1:3]
        context = super().get_context_data(**kwargs)
        context['title'] = 'Blog | All Categories'
        context['editors_first'] = editors_first
        context['editors_pick'] = editors_pick
        context['trending_posts'] = trending_posts
        context['latest_posts'] = latest_posts
        context["tags_active"] = True
        return context


class CategoryPostList(ListView):
    context_object_name = 'category_posts'
    paginate_by = 8
    template_name = 'blog/category-posts.html'

    def get_queryset(self):
        category = get_object_or_404(
            Category, name=self.kwargs.get('name'))
        return Post.objects.filter(publish=True, categories=category)

    def get_context_data(self, **kwargs):
        category = get_object_or_404(
            Category, name=self.kwargs.get('name'))
        context = super().get_context_data(**kwargs)
        context['category_name'] = category
        context['view_name'] = f"Posts on {category}"
        return context


class UsersFav(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    paginate_by = 8
    model = Post
    template_name = 'blog/user-favourites.html'

    def get_queryset(self):
        return Post.objects.filter(publish=True, favourites=self.request.user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"{self.request.user} | favourite posts"
        context['view_name'] = "Favourites Posts"
        return context

# class ReplyComment(LoginRequiredMixin,CreateView):


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post-details.html'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("blog:post-details", kwargs={'slug': post.slug}))
        return redirect(reverse("blog:post-details", kwargs={'slug': post.slug}))

    def get_context_data(self, **kwargs):
        post = self.get_object()
        cats_name = post.categories.all()
        similar_posts = Post.objects.filter(
            publish=True, categories__in=cats_name).exclude(slug=post.slug)[:3]
        latest_posts = Post.objects.filter(
            publish=True).exclude(slug=post.slug)[:4]
        author_posts = Post.objects.filter(
            publish=True, author=post.author).exclude(slug=post.slug)[:4]
        context = super().get_context_data(**kwargs)
        context['author_posts'] = author_posts
        context['latest_posts'] = latest_posts
        context['similar_posts'] = similar_posts
        context['form'] = CommentForm()
        return context


class PostComments(ListView):
    template_name = 'blog/post-comments.html'
    context_object_name = 'post_comments'
    paginate_by = 5

    def get_queryset(self):
        post = get_object_or_404(
            Post, slug=self.kwargs.get('slug'))
        return Comment.objects.filter(post=post, show=True)

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post = get_object_or_404(
            Post, slug=self.kwargs.get('slug'))
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("blog:post-comments", kwargs={'slug': post.slug}))
        # return redirect(reverse("blog:post-comments", kwargs={'slug': post.slug}))

    def get_context_data(self, **kwargs):
        post = get_object_or_404(
            Post, slug=self.kwargs.get('slug'))
        latest_posts = Post.objects.filter(
            publish=True).exclude(slug=post.slug)[:4]
        context = super().get_context_data(**kwargs)
        context["post"] = post
        context['form'] = CommentForm()
        context['latest_posts'] = latest_posts
        context["view_name"] = f"{post.title}"
        context["title"] = f"comments | {post.title}"
        return context


class PostCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post-form.html'
    success_message = 'Post added'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create post'
        context['create_post'] = 'create_post'
        context['title'] = 'Create post'
        context['create_post_link'] = 'active_link'
        context['addpost_active'] = True
        context['post_submit'] = 'Post'
        context['view_name'] = 'Create Post'
        context['add_active'] = True
        return context


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Post
    template_name = 'blog/post-form.html'
    form_class = PostForm
    success_message = 'Post updated'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True

    def get_context_data(self, **kwargs):
        post = self.get_object()
        context = super().get_context_data(**kwargs)
        context['title'] = post.title
        context['post_submit'] = 'Update'
        context['view_name'] = 'Update Post'
        return context


# class RedirectComment(LoginRequiredMixin,RedirectView):


class PostSearch(ListView):
    paginate_by = 1
    template_name = 'blog/post-search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        queryset = Post.objects.filter(publish=True,)
        search_form = SearchForm(self.request.GET or None)
        if search_form.is_valid():
            search = self.request.GET.get('search')
        return queryset.filter(
            Q(title__icontains=search)).distinct()

    def get_context_data(self, **kwargs):
        search = self.request.GET.get('search')
        context = super().get_context_data(**kwargs)
        context["title"] = 'Webblog | Search articles'
        context["search_words"] = search
        context["search_form"] = SearchForm(self.request.GET or None)
        return context
