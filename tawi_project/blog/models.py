from django.db import models
from django.utils import timezone
from users.models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from PIL import Image


class post(models.Model):


    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cover = models.ImageField(default='default2.jpg', upload_to='blog_pics')
    likes = models.ManyToManyField(CustomUser, related_name='post_likes', blank=True)
    comments = models.ManyToManyField(CustomUser, through='Comment', related_name='post_comments', blank=True)
    view_count = models.PositiveIntegerField(default=0)




    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs = {'pk': self.pk })

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.user.username} on {self.post.title}'




