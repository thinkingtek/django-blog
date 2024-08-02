from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    email = models.EmailField(verbose_name='Email Address', max_length=180, unique=True, help_text='Use a valid email address', error_messages={
                              'unique': 'Sorry this email cannot be used'})

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # bio = models.CharField(max_length=100)

    image = models.ImageField(
        default='profile_pix/profile_img.png', blank=True, null=True, upload_to='profile_pix', validators=[
            FileExtensionValidator(['jpg', 'jpeg'])])

    def save(self):
        super().save()
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    def __str__(self):
        return self.user.username
