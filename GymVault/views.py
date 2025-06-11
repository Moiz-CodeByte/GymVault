from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.backends import ModelBackend
from .models import Gym, User, GymAdmin, MembershipPlan, Member, Payment, Locker
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from gymvault.forms import RequestFormForm

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
        if request.user.phone is None or request.user.phone == '':
            return redirect('select_gym_plan')
        
        
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
   
        
        
    elif request.user.role == 'gymadmin':
        # Get the gym admin's gym
        try:
            gym_admin = GymAdmin.objects.get(user=request.user)
            gym = gym_admin.gym
            
            # Get all members for this gym
            members = Member.objects.filter(gym=gym)
            
            # Calculate expiry dates and active status
            for member in members:
                if member.start_date and member.membership_plan:
                    member.expiry_date = member.start_date + timedelta(days=member.membership_plan.duration_in_days)
                    member.is_expired = member.expiry_date < datetime.now().date()
                    if member.is_expired:
                        member.is_active = False
                        member.save()
            
            # Get all lockers for this gym
            lockers = Locker.objects.filter(gym=gym)
            
            # Get membership plans for this gym
            membership_plans = MembershipPlan.objects.filter(gym=gym)
            
            # Calculate statistics
            total_members = members.count()
            active_memberships = members.filter(is_active=True).count()
            available_lockers = lockers.filter(is_available=True).count()
            
            context = {
                'gym': gym,  # Add gym to context
                'members': members,
                'lockers': lockers,
                'membership_plans': membership_plans,
                'total_members': total_members,
                'active_memberships': active_memberships,
                'available_lockers': available_lockers,
            }
            return render(request, 'gymadmin_dashboard.html', context)
            
        except GymAdmin.DoesNotExist:
            messages.error(request, 'Gym admin profile not found.')
            return redirect('home')
            
    elif request.user.role == 'superadmin':
        return redirect('admin:index')
    else:
        return redirect('login')

@login_required
def member_detail(request, member_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    try:
        gym_admin = GymAdmin.objects.get(user=request.user)
        member = Member.objects.get(id=member_id, gym=gym_admin.gym)
        
        # Get member's payment history
        payments = Payment.objects.filter(member=member).order_by('-payment_date')
        
        # Calculate expiry date
        if member.start_date and member.membership_plan:
            member.expiry_date = member.start_date + timedelta(days=member.membership_plan.duration_in_days)
            member.is_expired = member.expiry_date < datetime.now().date()
            if member.is_expired:
                member.is_active = False
                member.save()
        
        context = {
            'member': member,
            'payments': payments,
        }
        return render(request, 'member_detail.html', context)
        
    except (GymAdmin.DoesNotExist, Member.DoesNotExist):
        messages.error(request, 'Member not found.')
        return redirect('dashboard')

@login_required
def deactivate_member(request, member_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    try:
        gym_admin = GymAdmin.objects.get(user=request.user)
        member = Member.objects.get(id=member_id, gym=gym_admin.gym)
        
        member.is_active = False
        member.save()
        
        messages.success(request, f'Member {member.user.get_full_name()} has been deactivated.')
    except (GymAdmin.DoesNotExist, Member.DoesNotExist):
        messages.error(request, 'Member not found.')
        
    return redirect('dashboard')

@login_required
def assign_locker(request, locker_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            gym_admin = GymAdmin.objects.get(user=request.user)
            locker = Locker.objects.get(id=locker_id, gym=gym_admin.gym)
            member_id = request.POST.get('member_id')
            
            if not locker.is_available:
                messages.error(request, 'Locker is already assigned.')
                return redirect('dashboard')
                
            member = Member.objects.get(id=member_id, gym=gym_admin.gym)
            
            # Check if member already has a locker
            existing_locker = Locker.objects.filter(assigned_member=member).first()
            if existing_locker:
                messages.error(request, f'Member already has locker {existing_locker.locker_number}. Please unassign it first.')
                return redirect('dashboard')
            
            locker.assigned_member = member
            locker.is_available = False
            locker.save()
            
            messages.success(request, f'Locker {locker.locker_number} has been assigned to {member.user.get_full_name()}.')
        except (GymAdmin.DoesNotExist, Locker.DoesNotExist, Member.DoesNotExist):
            messages.error(request, 'Invalid locker or member.')
            
    return redirect('dashboard')

@login_required
def unassign_locker(request, locker_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    try:
        gym_admin = GymAdmin.objects.get(user=request.user)
        locker = Locker.objects.get(id=locker_id, gym=gym_admin.gym)
        
        if locker.is_available:
            messages.error(request, 'Locker is not assigned.')
            return redirect('dashboard')
            
        member_name = locker.assigned_member.user.get_full_name()
        locker.assigned_member = None
        locker.is_available = True
        locker.save()
        
        messages.success(request, f'Locker {locker.locker_number} has been unassigned from {member_name}.')
    except (GymAdmin.DoesNotExist, Locker.DoesNotExist):
        messages.error(request, 'Locker not found.')
        
    return redirect('dashboard')

@login_required
def renew_membership(request, member_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            gym_admin = GymAdmin.objects.get(user=request.user)
            member = Member.objects.get(id=member_id, gym=gym_admin.gym)
            membership_plan_id = request.POST.get('membership_plan')
            
            membership_plan = MembershipPlan.objects.get(id=membership_plan_id, gym=gym_admin.gym)
            
            # Update membership
            member.membership_plan = membership_plan
            member.start_date = datetime.now().date()
            member.is_active = True
            member.save()
            
            # Create new payment
            Payment.objects.create(
                member=member,
                amount=membership_plan.price,
                payment_method='cash',
                status='pending'
            )
            
            messages.success(request, f'Membership renewed for {member.user.get_full_name()}.')
        except (GymAdmin.DoesNotExist, Member.DoesNotExist, MembershipPlan.DoesNotExist):
            messages.error(request, 'Invalid member or membership plan.')
            
    return redirect('dashboard')

@login_required
def update_membership(request, member_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            gym_admin = GymAdmin.objects.get(user=request.user)
            member = Member.objects.get(id=member_id, gym=gym_admin.gym)
            membership_plan_id = request.POST.get('membership_plan')
            
            membership_plan = MembershipPlan.objects.get(id=membership_plan_id, gym=gym_admin.gym)
            
            # Update membership
            member.membership_plan = membership_plan
            member.save()
            
            messages.success(request, f'Membership updated for {member.user.get_full_name()}.')
        except (GymAdmin.DoesNotExist, Member.DoesNotExist, MembershipPlan.DoesNotExist):
            messages.error(request, 'Invalid member or membership plan.')
            
    return redirect('dashboard')

@login_required
def delete_membership(request, member_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    try:
        gym_admin = GymAdmin.objects.get(user=request.user)
        member = Member.objects.get(id=member_id, gym=gym_admin.gym)
        
        # Unassign locker if assigned
        locker = Locker.objects.filter(assigned_member=member).first()
        if locker:
            locker.assigned_member = None
            locker.is_available = True
            locker.save()
        
        member.delete()
        messages.success(request, 'Membership deleted successfully.')
    except (GymAdmin.DoesNotExist, Member.DoesNotExist):
        messages.error(request, 'Member not found.')
        
    return redirect('dashboard')

@login_required
def add_locker(request):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            gym_admin = GymAdmin.objects.get(user=request.user)
            locker_number = request.POST.get('locker_number')
            
            Locker.objects.create(
                gym=gym_admin.gym,
                locker_number=locker_number,
                is_available=True
            )
            
            messages.success(request, f'Locker {locker_number} added successfully.')
        except GymAdmin.DoesNotExist:
            messages.error(request, 'Gym admin profile not found.')
            
    return redirect('dashboard')

@login_required
def update_locker(request, locker_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            gym_admin = GymAdmin.objects.get(user=request.user)
            locker = Locker.objects.get(id=locker_id, gym=gym_admin.gym)
            locker_number = request.POST.get('locker_number')
            
            locker.locker_number = locker_number
            locker.save()
            
            messages.success(request, f'Locker updated successfully.')
        except (GymAdmin.DoesNotExist, Locker.DoesNotExist):
            messages.error(request, 'Locker not found.')
            
    return redirect('dashboard')

@login_required
def delete_locker(request, locker_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    try:
        gym_admin = GymAdmin.objects.get(user=request.user)
        locker = Locker.objects.get(id=locker_id, gym=gym_admin.gym)
        
        if locker.assigned_member:
            messages.error(request, 'Cannot delete assigned locker. Please unassign it first.')
            return redirect('dashboard')
            
        locker.delete()
        messages.success(request, 'Locker deleted successfully.')
    except (GymAdmin.DoesNotExist, Locker.DoesNotExist):
        messages.error(request, 'Locker not found.')
        
    return redirect('dashboard')

@login_required
def update_payment_status(request, payment_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            gym_admin = GymAdmin.objects.get(user=request.user)
            payment = Payment.objects.get(id=payment_id, member__gym=gym_admin.gym)
            new_status = request.POST.get('status')
            
            if new_status in dict(Payment.PAYMENT_STATUS):
                payment.status = new_status
                payment.save()
                
                # Update member status based on payment
                if new_status == 'paid':
                    payment.member.is_active = True
                elif new_status == 'failed':
                    payment.member.is_active = False
                payment.member.save()
                
                messages.success(request, 'Payment status updated successfully.')
            else:
                messages.error(request, 'Invalid payment status.')
        except (GymAdmin.DoesNotExist, Payment.DoesNotExist):
            messages.error(request, 'Payment not found.')
            
    return redirect('member_detail', member_id=payment.member.id)

@login_required
def add_membership_plan(request):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            gym_admin = GymAdmin.objects.get(user=request.user)
            name = request.POST.get('name')
            price = request.POST.get('price')
            duration_in_days = request.POST.get('duration_in_days')
            
            MembershipPlan.objects.create(
                gym=gym_admin.gym,
                name=name,
                price=price,
                duration_in_days=duration_in_days
            )
            
            messages.success(request, 'Membership plan added successfully.')
        except GymAdmin.DoesNotExist:
            messages.error(request, 'Gym admin profile not found.')
        except Exception as e:
            messages.error(request, f'Error adding membership plan: {str(e)}')
            
    return redirect('dashboard')

@login_required
def update_membership_plan(request, plan_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        try:
            gym_admin = GymAdmin.objects.get(user=request.user)
            plan = MembershipPlan.objects.get(id=plan_id, gym=gym_admin.gym)
            
            plan.name = request.POST.get('name')
            plan.price = request.POST.get('price')
            plan.duration_in_days = request.POST.get('duration_in_days')
            plan.save()
            
            messages.success(request, 'Membership plan updated successfully.')
        except (GymAdmin.DoesNotExist, MembershipPlan.DoesNotExist):
            messages.error(request, 'Plan not found.')
        except Exception as e:
            messages.error(request, f'Error updating membership plan: {str(e)}')
            
    return redirect('dashboard')

@login_required
def delete_membership_plan(request, plan_id):
    if request.user.role != 'gymadmin':
        return redirect('dashboard')
        
    try:
        gym_admin = GymAdmin.objects.get(user=request.user)
        plan = MembershipPlan.objects.get(id=plan_id, gym=gym_admin.gym)
        
        # Check if plan is in use
        if Member.objects.filter(membership_plan=plan).exists():
            messages.error(request, 'Cannot delete plan that is currently in use.')
            return redirect('dashboard')
            
        plan.delete()
        messages.success(request, 'Membership plan deleted successfully.')
    except (GymAdmin.DoesNotExist, MembershipPlan.DoesNotExist):
        messages.error(request, 'Plan not found.')
    except Exception as e:
        messages.error(request, f'Error deleting membership plan: {str(e)}')
        
    return redirect('dashboard')

def about(request):
    return render(request, 'about.html')

def gyms_and_plans(request):
    gyms = Gym.objects.all()
    # Get membership plans for each gym
    for gym in gyms:
        gym.plans = MembershipPlan.objects.filter(gym=gym)
    return render(request, 'gyms_and_plans.html', {'gyms': gyms})


def request_form(request):
    if request.method == 'POST':
        form = RequestFormForm(request.POST)
        if form.is_valid():
            # Process the form data
            form.save()
            
            messages.success(request, 'Your request has been submitted successfully!')
            return redirect('home')
        
        
        
    form = RequestFormForm()
    return render(request, 'request_form.html', {'form': form})  

