import os
import django
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctorfinder.settings')
django.setup()

from django.contrib.auth import get_user_model
from pages.models import AdminStaff

User = get_user_model()

# Dictionary to map permission codes to display names
PERMISSION_DISPLAY = {
    'full': 'Full Admin Access',
    'doctors': 'Manage Doctors',
    'content': 'Manage Content',
    'users': 'Manage Users',
    'reviews': 'Manage Reviews'
}

def count_admin_users():
    # Count superusers
    superusers = User.objects.filter(is_superuser=True)
    print(f"Total superusers: {superusers.count()}")
    
    # Count staff users
    staff_users = User.objects.filter(is_staff=True, is_superuser=False)
    print(f"Total staff users (not superusers): {staff_users.count()}")
    
    # Count AdminStaff entries
    admin_staff = AdminStaff.objects.all()
    print(f"Total AdminStaff entries: {admin_staff.count()}")
    
    # Display detailed information
    print("\n=== Superusers ===")
    for user in superusers:
        last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "Never"
        print(f"- {user.get_full_name()} ({user.email})")
        print(f"  Username: {user.username}")
        print(f"  Last login: {last_login}")
        print(f"  Date joined: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Is doctor: {'Yes' if user.is_doctor else 'No'}")
        print("")
    
    print("\n=== Staff Users ===")
    for user in staff_users:
        last_login = user.last_login.strftime("%Y-%m-%d %H:%M:%S") if user.last_login else "Never"
        print(f"- {user.get_full_name()} ({user.email})")
        print(f"  Username: {user.username}")
        print(f"  Last login: {last_login}")
        print(f"  Date joined: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Is doctor: {'Yes' if user.is_doctor else 'No'}")
        print("")
    
    print("\n=== Admin Staff Records ===")
    if admin_staff.count() == 0:
        print("No Admin Staff records found.")
    else:
        for staff in admin_staff:
            created_at = staff.created_at.strftime("%Y-%m-%d %H:%M:%S")
            added_by = staff.added_by.get_full_name() if staff.added_by else "Unknown"
            permission_display = PERMISSION_DISPLAY.get(staff.permissions, staff.permissions)
            print(f"- {staff.user.get_full_name()} ({staff.user.email})")
            print(f"  Username: {staff.user.username}")
            print(f"  Role: {staff.role}")
            print(f"  Permissions: {permission_display}")
            print(f"  Is active: {'Yes' if staff.is_active else 'No'}")
            print(f"  Added by: {added_by}")
            print(f"  Created at: {created_at}")
            print("")

if __name__ == "__main__":
    count_admin_users() 