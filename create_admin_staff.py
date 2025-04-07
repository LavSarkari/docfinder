import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctorfinder.settings')
django.setup()

from django.contrib.auth import get_user_model
from pages.models import AdminStaff

User = get_user_model()

def sync_admin_staff_records():
    """Ensures all superusers have proper AdminStaff records"""
    
    # Get all superusers
    superusers = User.objects.filter(is_superuser=True)
    print(f"Found {superusers.count()} superusers")
    
    # Counter for created records
    created_count = 0
    
    for user in superusers:
        # Check if user already has an AdminStaff record
        try:
            admin_staff = AdminStaff.objects.get(user=user)
            print(f"AdminStaff record already exists for {user.get_full_name()} ({user.email})")
        except AdminStaff.DoesNotExist:
            # Create a new AdminStaff record
            admin_staff = AdminStaff.objects.create(
                user=user,
                role='Site Administrator',
                permissions='full',
                is_active=True,
                added_by=user  # Self-reference as the creator
            )
            created_count += 1
            print(f"Created new AdminStaff record for {user.get_full_name()} ({user.email})")
    
    print(f"\nSummary: Created {created_count} new AdminStaff records")
    print("All superusers now have proper AdminStaff records.")

if __name__ == "__main__":
    sync_admin_staff_records() 