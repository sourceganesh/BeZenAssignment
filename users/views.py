from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.forms.utils import ErrorList
from django.http import HttpResponse
from .forms import LoginForm, SignUpForm
from django.contrib import messages
from django.views.generic import TemplateView
from django.contrib.auth import logout

from django.shortcuts import render, redirect

from django.views import View

from users.forms import ProfileForm, form_validation_error
from users.models import UserProfile


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("users:view_profile", username=username)
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "users/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="users/login">login</a>.'
            success = True

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "users/register.html", {"form": form, "msg": msg, "success": success})


def view_profile(request, username):
    profile = UserProfile.objects.filter(user__username=username).first()
    if profile:
        return render(request, "users/view_profile.html", {'profile':profile})
    else:
        return redirect('users:profile')

def edit_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if form.is_valid():
                profile = form.save()
                profile.user.first_name = form.cleaned_data.get('first_name')
                profile.user.last_name = form.cleaned_data.get('last_name')
                profile.user.email = form.cleaned_data.get('email')
                profile.user.save()
                messages.success(request, 'Profile saved successfully')
            else:
                messages.error(request, form_validation_error(form))
            return redirect('users:edit_profile')
        else:
            form = ProfileForm(instance=request.user.profile)
        return render(request, 'users/edit_profile.html', {"form":form})
    else:
        return redirect('users:login')

def logout_page(request):
    logout(request)
    return render(request,'users/logout.html')