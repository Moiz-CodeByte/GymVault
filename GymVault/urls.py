from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    #path('', views.index, name='index'),
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('member/dashboard/', views.member_dashboard, name='member_dashboard'),
]
