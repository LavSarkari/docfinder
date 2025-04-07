from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from django.utils.translation import gettext as _
from django.contrib import messages

class CustomAccountAdapter(DefaultAccountAdapter):
    def pre_login(
        self,
        request,
        user,
        *,
        email_verification,
        signal_kwargs,
        email,
        signup,
        redirect_url
    ):
        """
        Custom pre_login handler to avoid sending verification emails 
        for already verified emails or for admin users.
        """
        # Allow admin users to bypass verification completely
        if user.is_superuser or user.is_staff:
            return None  # No block to login for admins
            
        if email_verification == "mandatory":
            # Check if the email is already verified
            email_address = EmailAddress.objects.filter(
                user=user, email=email, verified=True
            ).exists()

            # If email is already verified, allow login without verification
            if email_address:
                return None  # No block to login

        # Continue with default behavior for unverified emails
        return super().pre_login(
            request,
            user,
            email_verification=email_verification,
            signal_kwargs=signal_kwargs,
            email=email,
            signup=signup,
            redirect_url=redirect_url
        ) 