from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    cover = models.ImageField(default='default2.jpg', upload_to='blog_pics')






    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('post-detail', kwargs = {'pk': self.pk })

class Resume(models.Model):
    file = models.FileField(upload_to='resumes')
