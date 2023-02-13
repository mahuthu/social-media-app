from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.home, name="blogs-home"),
    path('about/', views.about, name="blogs-about"),

]
