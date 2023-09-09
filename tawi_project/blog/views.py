from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import post
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import FileResponse
from .models import Resume
from django.shortcuts import render, redirect






# Create your views here.




#we are using the class based view PostListView
def home(request):
    context = {'posts': post.objects.all()}
    return render(request, "blog/home.html", context)

class PostListView(ListView):
    model = post
    template_name = 'blog/blogpage.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5



#new list view with custom filtered queries
class UserPostListView(ListView):
    model = post
    template_name = 'blog/user_post.html'  #<app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username =self.kwargs.get('username'))
        return post.objects.filter(author = user).order_by('-date_posted')
class PostDetailView(DetailView):
    model = post

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

def index(request):
    return render(request, 'blog/index.html', {'title': 'index'})


def about(request):
    return render(request, 'blog/aboutus.html', {'title': 'about'})

def services(request):
    return render(request, 'blog/services.html', {'title': 'services'})

def contact(request):
    return render(request, 'blog/contact.html', {'title': 'contact'})


def resume_download(request):
    resume = get_object_or_404(Resume)
    file_path = resume.file.path
    response = FileResponse(open(file_path, 'rb'))
    return response








