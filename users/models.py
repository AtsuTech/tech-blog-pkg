from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


# extend user model
class User(AbstractUser):
    avatar = models.ImageField(verbose_name='avatar', upload_to='avatars/', null=True, blank=True)
    introduction = models.CharField(verbose_name='introduction', max_length=30)