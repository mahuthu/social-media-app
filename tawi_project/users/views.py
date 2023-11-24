from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.views import LoginView
from .models import CustomUser, Follow
from blog.models import post
import stripe
from django.http import HttpResponse
import os







# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            zip_code = form.cleaned_data.get('zip_code')

            # Create and save a CustomUser object
            user = CustomUser(username=username, email=email, zip_code=zip_code)
            user.set_password(zip_code)  # Set zip_code as the password
            user.save()

            messages.success(request, f'Account for {username} has been created. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



def custom_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST )
        print("form is valid")
        if form.is_valid():
            user = form.get_user()
            print("user is valid")
            if user is not None:
                login(request, user)
                # Redirect to the home page or another desired URL after successful login
                return redirect('blogs-home')
                print("user is valid")
            else:
                # Handle invalid login credentials
                return render(request, 'users/login.html', {'form': form, 'error_message': 'Invalid username or password'})
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required()
def profile(request):
    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():

            u_form.save()
            p_form.save()
            messages.success(request, f"your profile has been updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context = {'u_form': u_form, 'p_form': p_form }

    return render(request, "users/profile.html", context)







@login_required
def follow_user(request, username):
    user_to_follow = CustomUser.objects.get(username=username)

    # Check if the user is not trying to follow themselves
    if request.user != user_to_follow:
        _, created = Follow.objects.get_or_create(follower=request.user, following=user_to_follow)

    # Redirect back to the same page
    return redirect(request.GET.get('next', 'blog/blogs-home'))


@login_required
def unfollow_user(request, username):
    user_to_unfollow = CustomUser.objects.get(username=username)

    # Check if the user is not trying to unfollow themselves
    if request.user != user_to_unfollow:
        Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()

    # Redirect back to the same page
    return redirect(request.GET.get('next', 'users/following_list'))

@login_required
def following_list(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    users = CustomUser.objects.filter(id__in=following_users)
    
    context = {'following_users': users}
    return render(request, 'users/following_list.html', context)




    
