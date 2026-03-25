from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, "home.html")

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        email = request.POST.get("mail")
        password = request.POST.get("password")

        if not name or not contact or not email or not password :
            messages.error(request, "Fill all the Fields to continue!")
            return redirect("signup-view")
        
        if len(password) < 6:
            messages.error(request, "Password length is invalid!")
            return redirect("signup-view")
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email Already exist!")
            return redirect("signup-view")
        
        user = User.objects.create_user(username=email, password=password)
        if " " in name:
            first,last = name.split(" ",1)
        else :
            first, last = name, ""
        
        user.first_name , user.last_name = first, last
        user.save()
        UserProfile.objects.create(user=user, phone = contact)
        login(request, user)
        messages.success(request, "Account Created Successfully :)")
        # can also redirect to login page from here
        return redirect("predict-view")


    return render(request, "signup.html")

@login_required
def prediction(request):
    return render(request, "predict.html")

def logout_page(request):
    logout(request)
    messages.success(request, "LogOut Successfully!")
    return redirect("login-view")

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get("mail")
        password = request.POST.get("password")
        user = authenticate(request, username = email, password = password)

        if user is not None:
            login(request,user)
            messages.success(request, "Login Successfully :)")
            return redirect("predict-view")
        else:
            messages.error(request, "Invalid Email or Password !")
    return render(request, "login.html")
