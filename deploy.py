#!/usr/bin/env python
"""
Deployment script for DoctorFinder on AlwaysData hosting
Run this after uploading your project files to set up the environment
"""

import os
import sys
import subprocess
import random
import string
import time

def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    
    # Print output in real-time
    while True:
        output = process.stdout.readline().decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    return process.poll()

def generate_secret_key(length=50):
    """Generate a random secret key"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def create_directories():
    """Create necessary directories if they don't exist"""
    print("\n----- Creating directories -----\n")
    dirs = [
        'media',
        'staticfiles',
        'logs',
    ]
    
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")

def test_database_connection():
    """Test the database connection"""
    print("\n----- Testing database connection -----\n")
    
    try:
        import psycopg2
        
        # Get database settings from settings.py
        import django
        from django.conf import settings
        
        db_settings = settings.DATABASES['default']
        
        print(f"Connecting to database: {db_settings['NAME']} on {db_settings['HOST']}...")
        
        conn = psycopg2.connect(
            dbname=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            host=db_settings['HOST'],
            port=db_settings['PORT'],
        )
        
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        
        print(f"Database connection successful!")
        print(f"PostgreSQL version: {db_version[0]}")
        
        cur.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("\nTroubleshooting steps:")
        print("1. Verify database credentials in settings.py")
        print("2. Make sure the database exists")
        print("3. Check if you can connect from the AlwaysData admin panel")
        return False

def test_email_setup():
    """Test the email setup by asking to send a test email"""
    print("\n----- Email Configuration Test -----\n")
    
    print("Would you like to test the email configuration? (y/n)")
    choice = input().strip().lower()
    
    if choice != 'y':
        print("Skipping email test.")
        return
    
    try:
        print("\nThis will send a test email to verify configuration.")
        recipient = input("Enter recipient email address: ")
        
        from django.core.mail import send_mail
        from django.conf import settings
        
        subject = 'DoctorFinder Email Configuration Test'
        message = 'This is a test email from DoctorFinder. If you received this, the email configuration is working correctly.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [recipient]
        
        print(f"Sending test email from {from_email} to {recipient}...")
        
        result = send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )
        
        if result:
            print("\nEmail sent successfully!")
            print("Please check your inbox (and spam folder) to confirm receipt.")
        else:
            print("\nFailed to send email. Check the email settings in your configuration.")
            
    except Exception as e:
        print(f"\nError testing email: {e}")
        print("\nTroubleshooting steps:")
        print("1. Verify email settings in production_settings.py")
        print("2. Check if your AlwaysData email account is active")
        print("3. Try sending an email through the webmail interface")

def main():
    """Main deployment function"""
    print("\n===== DoctorFinder Deployment Script =====\n")
    
    # Define paths
    project_dir = os.path.dirname(os.path.abspath(__file__))
    settings_file = os.path.join(project_dir, 'doctorfinder', 'settings.py')
    prod_settings_file = os.path.join(project_dir, 'production_settings.py')
    
    # 1. Create necessary directories
    create_directories()
    
    # 2. Install dependencies
    print("\n----- Installing dependencies -----\n")
    run_command("pip install --user -r requirements.txt")
    
    # 3. Generate and update secret key
    print("\n----- Generating secret key -----\n")
    secret_key = generate_secret_key()
    
    # Read production settings
    with open(prod_settings_file, 'r') as f:
        settings_content = f.read()
    
    # Replace placeholder with new secret key
    settings_content = settings_content.replace(
        "SECRET_KEY = 'your-production-secret-key-here'",
        f"SECRET_KEY = '{secret_key}'"
    )
    
    # Write back to production settings
    with open(prod_settings_file, 'w') as f:
        f.write(settings_content)
    
    # Copy production settings to settings.py
    with open(settings_file, 'w') as f:
        f.write(settings_content)
    
    print("Secret key generated and settings updated!")
    
    # 4. Set Django settings module for the script
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctorfinder.settings')
    
    # Need to give time for the settings to be recognized
    time.sleep(2)
    
    # 5. Test database connection
    db_ok = test_database_connection()
    
    if not db_ok:
        print("\nWARNING: Database connection failed.")
        print("Would you like to continue with deployment anyway? (y/n)")
        choice = input().strip().lower()
        if choice != 'y':
            print("Deployment aborted. Please fix database issues and try again.")
            return
    
    # 6. Set up database
    print("\n----- Setting up database -----\n")
    run_command("python manage.py migrate")
    
    # 7. Collect static files
    print("\n----- Collecting static files -----\n")
    run_command("python manage.py collectstatic --noinput")
    
    # 8. Create superuser (optional - can be skipped if you want to run it manually)
    print("\n----- Create superuser -----\n")
    print("You will need to create an admin superuser.")
    print("Would you like to create a superuser now? (y/n)")
    choice = input().strip().lower()
    
    if choice == 'y':
        run_command("python manage.py createsuperuser")
    else:
        print("Skipping superuser creation. You can create one later with 'python manage.py createsuperuser'")
    
    # 9. Test email configuration
    test_email_setup()
    
    # 10. Set proper permissions
    print("\n----- Setting file permissions -----\n")
    run_command("chmod -R 755 staticfiles")
    run_command("chmod -R 755 media")
    
    print("\n===== Deployment Complete! =====\n")
    print("Your DoctorFinder application should now be configured.")
    print("Access your site at: https://lavsarkari.alwaysdata.net")
    print("Access the admin at: https://lavsarkari.alwaysdata.net/admin/")
    print("Access webmail at: https://webmail.alwaysdata.com/")

if __name__ == "__main__":
    main() 