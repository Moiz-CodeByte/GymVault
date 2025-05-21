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
]
