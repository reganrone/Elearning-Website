
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomUserForm, AuthenticationFormWithRole
from .models import CustomUser

def index(request):
    context = {}
    return render(request, "users/index.html", context)

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('login')  # Redirect to the login page
    else:
        form = UserCreationForm()
    
    return render(request, "users/signup.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationFormWithRole(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            role = request.POST.get("role")  # Get the selected role from the form
            if role == "teacher":
                login(request, user)
                return redirect("teachers:home")  # Redirect to the teacher dashboard
            elif role == "student":
                login(request, user)
                return redirect("students:home")  # Redirect to the student dashboard
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def user_logout(request):
    logout(request)
    return redirect("index")  
