from django.forms import ModelForm
from .models import RequestForm
from django import forms

class RequestFormForm(ModelForm):
    class Meta:
        model = RequestForm
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-sm focus:outline-none focus:border-gray-400 dark:focus:border-gray-500 focus:bg-white dark:focus:bg-gray-600 mt-5'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-sm focus:outline-none focus:border-gray-400 dark:focus:border-gray-500 focus:bg-white dark:focus:bg-gray-600 mt-5'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-sm focus:outline-none focus:border-gray-400 dark:focus:border-gray-500 focus:bg-white dark:focus:bg-gray-600 mt-5'}),
            'message': forms.Textarea(attrs={'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 placeholder-gray-500 text-sm text-gray-900 dark:text-gray-100 focus:outline-none focus:border-gray-400 focus:bg-white dark:focus:bg-gray-800', 'rows': 3}),
        }