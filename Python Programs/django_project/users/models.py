from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=40, default='What\'s your gender?', blank=True)
    bio = models.TextField(default='Write Something About Yourself!', blank=True)
    location = models.CharField(max_length=100, default='Where are you from?', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
