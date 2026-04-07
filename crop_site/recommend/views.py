from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from .pkl_folder.loader import load_pkl, start_prediction
from django.utils import timezone
import json
from datetime import timedelta
from django.db.models import Count

# Create your views here.
def home(request):
    total_user = User.objects.filter(is_staff = False).count()
    total_prediction = Prediction.objects.count()
    return render(request, "home.html", locals())

def signup(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        email = request.POST.get("mail")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm")

        if not name or not contact or not email or not password :
            messages.error(request, "Fill all the Fields to continue!")
            return redirect("signup-view")
        
        if len(password) < 6:
            messages.error(request, "Password length is invalid!")
            return redirect("signup-view")
        
        if password != confirm_password:
            messages.error(request,"Passwords are not matching !")
            return redirect("signup-view")
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email Already exist!")
            return redirect("signup-view")
        
        if not contact.isdigit() or len(contact)<10:
            messages.error(request, "Invalid Contact Number")
            return redirect('signup-view')
        
        user = User.objects.create_user(username=email, password=password)
        if " " in name:
            parts = name.strip().split()
            first = parts[0]
            last = " ".join(parts[1:]) if len(parts) > 1 else ""
        else :
            first, last = name, ""
        
        user.first_name , user.last_name = first, last
        user.save()
        UserProfile.objects.create(user=user, phone = contact)
        login(request, user)
        messages.success(request, "Account Created Successfully :)")
        return redirect("predict-view")


    return render(request, "signup.html")


@login_required
def predicting(request):
    feature_order = load_pkl()["features"]
    result = None
    input_data = None

    if request.method == "POST":
        data = {}
        try:
            for f in feature_order:
                val = request.POST.get(f)
                if val is None or val == "":
                    raise ValueError
                else:
                    data[f] = float(val)

        except ValueError:
            messages.error(request, "Please enter valid inputs!")
            return redirect("predict-view")
        
        try:
            crop = start_prediction(data)
        except Exception:
            messages.error(request, "Prediction failed. Try again!")
            return redirect("predict-view")        
        
        Prediction.objects.create(user = request.user, predicted_label = crop, **data)
        result = crop
        input_data = data
        messages.success( request,f"Recommended Crop : {crop}")
    return render(request, "predict.html", locals())

@login_required
def history(request):
    prediction = Prediction.objects.filter(user=request.user)
    return render(request, "history.html", locals())

from django.shortcuts import get_object_or_404
@login_required
def delete_user_entry(request,id):
    pred = get_object_or_404(Prediction, id=id, user=request.user)
    pred.delete()
    messages.success(request,"Entry removed Successfully :)")
    return redirect("history-view")

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    name = request.user.get_full_name()

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        if name : 
            parts = name.split(" ",1)
            request.user.first_name = parts[0]
            request.user.last_name = parts[1] if len(parts) > 1 else ""
        user_profile.phone = phone
        request.user.save()
        user_profile.save()
        messages.success(request,"Profile Updated Successfully :)")
            
    return render(request, "profile.html", locals())

from django.contrib.auth import update_session_auth_hash
@login_required
def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm")
        if not request.user.check_password(current_password):
            messages.error(request, "Current Password is not matched!")
            return redirect("password-view")
        if len(password) < 6:
            messages.error(request, "Enter a valid length password!")
            return redirect("password-view")
        if password != confirm_password:
            messages.error(request,"Passwords are not matching !")
            return redirect("password-view")
        else:
            request.user.set_password(password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            # user = authenticate(request, username = request.user.username, password = password)
            # if user : 
            #     login(request,user)
            #     messages.success(request, "Password updated Successfully :)")
            #     return redirect("password-view")
            messages.success(request, "Password updated Successfully :)")
            return redirect("password-view")
    return render(request, "password.html", locals())
        

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


# Admin
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username = username, password = password)
        if not user:
            env_user = os.getenv('ADMIN_USERNAME')
            env_pass = os.getenv('ADMIN_PASSWORD')
            if username == env_user and password == env_pass:
                user, created = User.objects.get_or_create(username=username)
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
                user = authenticate(username=username, password=password)
                
        if not user :
            messages.error(request, "Invalid Credentials !")
            return redirect("admin-login-view")
        if not user.is_staff:
            messages.error(request, "You are not authenticated as admin!")
            return redirect("admin-login-view")
            
        login(request, user)
        messages.success(request, "Successfully Logedin as admin :)")
        return redirect("admin-dashboard-view")

    return render(request, "admin_login.html")

def staff(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(staff, login_url="admin-login-view")
def admin_dashboard(request):
    total_user = User.objects.filter(is_staff = False).count()
    total_prediction = Prediction.objects.count()

    crop_qs = Prediction.objects.values('predicted_label').annotate(c = Count('id')).order_by('-c')[:10]

    crop_labels = [i['predicted_label'] for i in crop_qs]
    crop_counts = [i['c'] for i in crop_qs]

    today = timezone.localdate()
    days = [today-timedelta(days=i) for i in range(6, -1, -1)]      # dates

    day_labels  = [d.strftime("%d %b") for d in days] # convert date to format : 03 Mar
    day_counts = [Prediction.objects.filter(created_at__date = d).count() for d in days] # prediction on d date

    context = {
        "total_user":total_user,
        "total_prediction":total_prediction,
        "crop_labels":json.dumps(crop_labels),
        "crop_counts":json.dumps(crop_counts),
        "day_labels":json.dumps(day_labels),
        "day_counts":json.dumps(day_counts),
    }

    return render(request, "admin_dashboard.html", context)

@user_passes_test(staff, login_url="admin-login-view")
def admin_users(request):
    users = User.objects.filter(is_staff = False)
    return render(request, "admin_users.html", {"users":users})

@login_required
def delete_user(request,id):
    user = get_object_or_404(User, id=id)
    user.delete()
    messages.success(request,"User removed Successfully :)")
    return redirect("admin-users-view")

from django.utils.dateparse import parse_date
@user_passes_test(staff, login_url="admin-login-view")
def admin_prediction(request):
    qs = Prediction.objects.select_related('user')
    
    crop = request.GET.get('crop')
    start = request.GET.get('end')
    end = request.GET.get('end')

    if crop:
        qs = qs.filter(predicted_label__iexact = crop)

    d_start = parse_date(start) if start else None
    d_end = parse_date(end) if end else None

    if d_start : 
        qs = qs.filter(created_at__date__gte = d_start)
    if d_end:
        qs = qs.filter(created_at__date__lte = d_end)
    
    crops = (Prediction.objects.order_by('predicted_label').values_list('predicted_label', flat = True).distinct())

    context = {
        "qs":qs,
        "crops" : crops,
        "current_crop":crop,
        "start":start,
        "end":end,
    }

    return render(request, "admin_prediction.html", context)

@user_passes_test(staff, login_url='admin-login-view')
def admin_delete_pred(request,id):
    pred = get_object_or_404(Prediction, id=id)
    pred.delete()
    messages.success(request,"Prediction deleted Successfully :)")
    return redirect("admin-prediction-view")

def admin_logout(request):
    logout(request)
    messages.success(request, "LogOut Successfully!")
    return redirect("admin-login-view")
