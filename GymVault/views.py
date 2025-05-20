from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .models import Gym, User, GymAdmin, MembershipPlan, Member, Payment, Locker
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
# def home(request):
#     return HttpResponse("Hello, World!")
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.user.is_authenticated:
        if request.user.role == 'superadmin':
            return redirect('admin:index')
        return redirect('dashboard')
 
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            if user.role == 'superadmin':
                return redirect('admin:index')
            return redirect('dashboard')
        
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def register(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    gyms = Gym.objects.all()
    context = {
        'gyms': gyms
    }
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']



        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,  email=email, password=password, role='member')
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome to GymVault, {username}!')
            return redirect('dashboard')
    return render(request, 'register.html', context)

def logout(request):
    auth_logout(request)
    return redirect('home')

def dashboard(request):
    if request.user.role == 'member':
        return render(request, 'member_dashboard.html')
    if request.user.role == 'gymadmin':
        return render(request, 'gymadmin_dashboard.html')
    elif request.user.role == 'superadmin':
       return redirect('admin/')
    else:
        return redirect('login')



# def get_all_gym(request):


