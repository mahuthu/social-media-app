from typing import Any
from django import http
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import post, Comment
from users.models import CustomUser
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.shortcuts import render, redirect
import requests
from django.http import HttpRequest, HttpResponse


# Create your views here.

class PostListView(ListView):
    model = post
    template_name = 'blog/blogpage.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(request, *args, **kwargs)

        free_post_count = request.session.get('free_post_count', 0)
        print(f"Free Post Count: {free_post_count}")
        
        if free_post_count < 20:
            request.session['free_post_count'] = free_post_count + 1
        else:
            return render(request, 'blog/paywall.html')

        return super().get(request, *args, **kwargs)

#new list view with custom filtered queries
class UserPostListView(LoginRequiredMixin, ListView):
    model = post
    template_name = 'blog/user_post.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username =self.kwargs.get('username'))
        return post.objects.filter(author = user).order_by('-date_posted')
    

class PostDetailView(DetailView):
    model = post
    template_name = 'blog/post_detail.html'  #<app>/<model>_<viewtype>.html

    def get(self, request, *args, **kwargs):
        # Retrieve the post instance
        post = self.get_object()

        # Increment the view_count
        post.view_count += 1
        post.save()

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = post
    fields = ['title', 'content', 'cover']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,  UpdateView):
    model = post
    fields = ['title', 'content', 'cover']

    def form_valid(self, form):
        form.instance.author = self.request.user
        cover = self.request.FILES.get('cover')

        # Check if a new cover image was uploaded
        if cover:
            # Save the cover image to the media root folder
            form.instance.cover = cover
            form.instance.save()

        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    success_url = '/home/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required
def like_post(request, pk):
    selected_post = get_object_or_404(post, pk=pk)

    if request.user in selected_post.likes.all():
        selected_post.likes.remove(request.user)
    else:
        selected_post.likes.add(request.user)

    return redirect('post-detail', pk=pk)

    
@login_required
def add_comment(request, pk):
    selected_post = get_object_or_404(post, pk=pk)

    if request.method == 'POST':
        text = request.POST.get('comment_text')
        Comment.objects.create(user=request.user, post=selected_post, text=text)

    return redirect('post-detail', pk=pk)

#def post_detail(request, pk):
   # post = get_object_or_404(post, pk=pk)

    # Increment the view_count only if the user is authenticated
    #if request.user.is_authenticated:
       # post.view_count += 1
       # post.save()

    #context = {'post': post}
    #return render(request, 'blog/post_detail.html', context)


