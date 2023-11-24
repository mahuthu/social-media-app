from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, CustomUser, Follow

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id','username', 'email', 'zip_code']

admin.site.register(Profile)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Follow)
# Register your models here.
