from django.urls import path
from.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, resume_download
from. import views
urlpatterns = [
    path('user/<str:username>', UserPostListView.as_view(), name="user-posts"),
    path('post/<int:pk>/', PostDetailView.as_view(), name="post-detail"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="post-delete"),
    path('aboutme/', views.about, name="blogs-about"),
    path('services/', views.services, name="blogs-services"),
    path('contact/', views.contact, name="blogs-contact"),
    path('index/', views.index, name="blogs-index"),
    path('resumes/', resume_download, name='resume_download'),


]
