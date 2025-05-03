from django.urls import path
from GymVault.views import home

urlpatterns = [
    path('', home, name='home'),
] 