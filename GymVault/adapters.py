from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        user.role = 'member'  # Set the role to member for all social logins
        user.save()
        return user
    
    def get_login_redirect_url(self, request):
        """
        Returns the default URL to redirect to after logging in.
        """
        return '/dashboard/'
    
    def get_signup_redirect_url(self, request):
        """
        Returns the default URL to redirect to after signing up.
        """
        return '/dashboard/'
        
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed.
        """
        # Bypass allauth's default redirect and force login
        user = sociallogin.user
        if user.id:
            # User is already authenticated, no need to go through signup
            sociallogin.state['process'] = 'login'
