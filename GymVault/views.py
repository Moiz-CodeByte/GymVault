from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.backends import ModelBackend
from .models import Gym, User, GymAdmin, MembershipPlan, Member, Payment, Locker
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

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
    if request.user.is_authenticated:
        return redirect('dashboard')
    
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

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            role='member'
        )
        
        if user is not None:
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome to GymVault, {username}!')
            return redirect('select_gym_plan')
            
    return render(request, 'register.html')

@login_required
def select_gym_plan(request):
    if request.user.role != 'member':
        return redirect('dashboard')
        
    gyms = Gym.objects.all()
    membership_plans = MembershipPlan.objects.all()
    
    context = {
        'gyms': gyms,
        'membership_plans': membership_plans,
    }
    return render(request, 'select_gym_plan.html', context)

@login_required
def complete_registration(request):
    if request.user.role != 'member':
        return redirect('dashboard')
        
    if request.method == 'POST':
        gym_id = request.POST.get('gym')
        membership_plan_id = request.POST.get('membership_plan')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        try:
            # Update user profile
            user = request.user
            user.phone = phone
            user.address = address
            user.save()
            
            # Get gym and plan
            gym = Gym.objects.get(id=gym_id)
            membership_plan = MembershipPlan.objects.get(id=membership_plan_id)
            
            # Create member record
            member = Member.objects.create(
                user=user,
                gym=gym,
                membership_plan=membership_plan,
                start_date=datetime.now().date(),
                is_active=True
            )
            
            # Create pending payment
            Payment.objects.create(
                member=member,
                amount=membership_plan.price,
                payment_method='cash',  # Default to bank transfer
                status='pending'
            )
            
            messages.success(request, 'Registration completed successfully! Please complete the payment to activate your membership.')
            return redirect('dashboard')
            
        except (Gym.DoesNotExist, MembershipPlan.DoesNotExist):
            messages.error(request, 'Invalid gym or membership plan selected.')
            return redirect('select_gym_plan')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return redirect('select_gym_plan')
            
    return redirect('select_gym_plan')

def logout(request):
    auth_logout(request)
    return redirect('home')

@login_required
def update_profile(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        user = request.user
        user.phone = phone
        user.address = address
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')
    
    return redirect('dashboard')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.user.role == 'member':
        # Get all memberships for the user
        memberships = Member.objects.filter(user=request.user)
        
        # Calculate expiry dates for memberships
        for membership in memberships:
            if membership.start_date and membership.membership_plan:
                membership.expiry_date = membership.start_date + timedelta(days=membership.membership_plan.duration_in_days)
                membership.is_expired = membership.expiry_date < datetime.now().date()
        
        # Get all payments for the user's memberships
        payments = Payment.objects.filter(member__user=request.user).order_by('-payment_date')
        
        # Get locker assignment if any
        locker = Locker.objects.filter(assigned_member__user=request.user).first()
        
        context = {
            'memberships': memberships,
            'payments': payments,
            'locker': locker,
        }
        return render(request, 'member_dashboard.html', context)
        
    if request.user.role == 'gymadmin':
        return render(request, 'gymadmin_dashboard.html')
    elif request.user.role == 'superadmin':
       return redirect('admin:index')
    else:
        return redirect('login')



# def get_all_gym(request):


