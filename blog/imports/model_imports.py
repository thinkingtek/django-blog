from django.db import models
from PIL import Image
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

User = get_user_model()
