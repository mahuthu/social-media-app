from django.contrib import admin
from .models import post
from .models import Comment

admin.site.register(post)
admin.site.register(Comment)

# Register your models here.
