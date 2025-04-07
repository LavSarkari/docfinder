import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctorfinder.settings')
django.setup()

from django.contrib.auth import get_user_model
from pages.models import AdminStaff

User = get_user_model()

def setup_main_admin():
    # Check if user exists
    try:
        user = User.objects.get(email='lavsarkari@doctorfinder.com')
        print(f"User with email lavsarkari@doctorfinder.com already exists.")
    except User.DoesNotExist:
        # Create the superuser
        user = User.objects.create_user(
            username='lavsarkari',
            email='lavsarkari@doctorfinder.com',
            password='Lav@Admin123',
            first_name='Lav',
            last_name='Sarkari',
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"Created superuser: Lav Sarkari (lavsarkari@doctorfinder.com)")
    
    # Check if admin profile exists
    try:
        admin_profile = AdminStaff.objects.get(user=user)
        print(f"Admin profile for Lav Sarkari already exists.")
    except AdminStaff.DoesNotExist:
        # Create admin profile
        admin_profile = AdminStaff.objects.create(
            user=user,
            role='Site Administrator',
            permissions='full',
            is_active=True,
            added_by=user  # Self-reference as the creator
        )
        print(f"Created admin profile for Lav Sarkari with full permissions.")
    
    print("\nLogin credentials:")
    print("Email: lavsarkari@doctorfinder.com")
    print("Password: Lav@Admin123")
    print("\nIMPORTANT: Change this password immediately after first login!")

if __name__ == "__main__":
    setup_main_admin() 