from .imports.model_imports import *


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(
        Category,  related_name='post_categories')
    image = models.ImageField(
        default='posts_img/post_default.jpeg', upload_to='posts_img', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', ])])
    title = models.CharField(max_length=130)
    slug = models.SlugField(max_length=220, unique=True, error_messages={
                            "unique": "Post with this slug dey"})
    # content = models.TextField()
    content = RichTextField()
    date_posted = models.DateTimeField(auto_now_add=True, editable=True)
    likes = models.ManyToManyField(User,
                                   default=None, blank=True, related_name='user_likes')
    favourites = models.ManyToManyField(User,
                                        default=None, blank=True, related_name='user_favourite')
    date_updated = models.DateTimeField(auto_now=True)
    edictors_pick = models.BooleanField(default=False)
    featured = models.BooleanField(default=True)
    publish = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("blog:post-details", kwargs={"slug": self.slug})

    def get_like_url(self):
        return reverse("blog:like-post", kwargs={"slug": self.slug})

    @property
    def get_comments(self):
        return self.comments.filter(show=True)

    @property
    def view_count(self):
        return PostView.objects.filter(post=self, show_view=True).count()

    @property
    def time_diff(self):
        if self.date_posted < self.date_updated:
            time = self.date_updated
            print(
                f'this is date: {self.date_posted} and this is update date: {self.date_updated}')
            return time

    class Meta:
        ordering = ['-date_posted']

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        if img.height > 420 or img.width > 420:
            output_size = (420, 420)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.title


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    show_view = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    show = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username} - {self.post}"
