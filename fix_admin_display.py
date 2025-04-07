import os
import django
from datetime import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctorfinder.settings')
django.setup()

from django.contrib.auth import get_user_model
from pages.models import AdminStaff

User = get_user_model()

def diagnose_admin_staff():
    """Diagnose and print detailed information about AdminStaff records"""
    
    print("=== Diagnose AdminStaff Records ===\n")
    
    # Get all AdminStaff records
    admin_staff = AdminStaff.objects.all()
    print(f"Total AdminStaff records: {admin_staff.count()}")
    
    if admin_staff.count() == 0:
        print("No AdminStaff records found.")
        return
    
    # Check if records exist
    for i, staff in enumerate(admin_staff, 1):
        print(f"\nRecord #{i}:")
        print(f"  ID: {staff.id}")
        print(f"  User: {staff.user.get_full_name()} ({staff.user.email})")
        print(f"  Username: {staff.user.username}")
        print(f"  Role: {staff.role}")
        print(f"  Permissions: {staff.permissions}")
        print(f"  Is active: {staff.is_active}")
        
        if staff.added_by:
            print(f"  Added by: {staff.added_by.get_full_name()} ({staff.added_by.email})")
        else:
            print("  Added by: None")
            
        print(f"  Created at: {staff.created_at}")
        
        # Check for data issues
        issues = []
        if not staff.role:
            issues.append("Missing role")
        if not staff.permissions:
            issues.append("Missing permissions")
        if not staff.added_by:
            issues.append("No creator reference")
        
        if issues:
            print("  Issues found: " + ", ".join(issues))
        else:
            print("  No issues found with this record")
    
    # Check for superusers without AdminStaff records
    superusers = User.objects.filter(is_superuser=True)
    admin_users = AdminStaff.objects.values_list('user_id', flat=True)
    
    missing_records = []
    for user in superusers:
        if user.id not in admin_users:
            missing_records.append(user)
    
    if missing_records:
        print("\n=== Superusers without AdminStaff records ===")
        for user in missing_records:
            print(f"- {user.get_full_name()} ({user.email})")
    else:
        print("\nAll superusers have AdminStaff records.")

if __name__ == "__main__":
    diagnose_admin_staff() 