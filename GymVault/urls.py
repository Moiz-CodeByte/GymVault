from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    #path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('select-gym-plan/', views.select_gym_plan, name='select_gym_plan'),
    path('complete-registration/', views.complete_registration, name='complete_registration'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('update-profile/', views.update_profile, name='update_profile'),
    
    # Gym Admin URLs
    path('gymadmin/member/<int:member_id>/', views.member_detail, name='member_detail'),
    path('gymadmin/member/<int:member_id>/renew/', views.renew_membership, name='renew_membership'),
    path('gymadmin/member/<int:member_id>/update/', views.update_membership, name='update_membership'),
    path('gymadmin/member/<int:member_id>/delete/', views.delete_membership, name='delete_membership'),
    path('gymadmin/locker/<int:locker_id>/assign/', views.assign_locker, name='assign_locker'),
    path('gymadmin/locker/<int:locker_id>/unassign/', views.unassign_locker, name='unassign_locker'),
    path('gymadmin/locker/<int:locker_id>/update/', views.update_locker, name='update_locker'),
    path('gymadmin/locker/<int:locker_id>/delete/', views.delete_locker, name='delete_locker'),
    path('gymadmin/locker/add/', views.add_locker, name='add_locker'),
    path('gymadmin/payment/<int:payment_id>/update-status/', views.update_payment_status, name='update_payment_status'),
]
