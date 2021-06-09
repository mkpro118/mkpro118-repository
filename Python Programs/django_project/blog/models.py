from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from blog.get_request import get_request


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='blog_post')

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def is_liked(self):
        return self.likes.filter(id=get_request().user.id).exists()

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
