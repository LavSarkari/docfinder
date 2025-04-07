#!/usr/bin/env python
"""
Test script for email functionality on AlwaysData
"""

import os
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_connection():
    """Test the email connection using AlwaysData SMTP"""
    
    print("\n===== Testing Email Connection =====\n")
    
    # Email settings for AlwaysData
    smtp_server = 'smtp-lavsarkari.alwaysdata.net'
    smtp_port = 587
    email_user = 'lavsarkari@alwaysdata.net'
    email_password = 'DataBase0808'
    recipient_email = input("Enter recipient email address to test: ")
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = recipient_email
    msg['Subject'] = 'DoctorFinder Email Test'
    
    # Add body
    body = """
    This is a test email from DoctorFinder.
    
    If you're receiving this, the email configuration is working correctly.
    
    Thank you,
    DoctorFinder Team
    """
    msg.attach(MIMEText(body, 'plain'))
    
    # Attempt to send email
    try:
        print(f"Connecting to {smtp_server}:{smtp_port}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        print(f"Logging in as {email_user}...")
        server.login(email_user, email_password)
        
        print(f"Sending test email to {recipient_email}...")
        text = msg.as_string()
        server.sendmail(email_user, recipient_email, text)
        
        server.quit()
        print("\nEmail sent successfully! Check the recipient's inbox.")
        print("If you don't see the email, check spam/junk folders.")
        
    except Exception as e:
        print(f"\nError sending email: {e}")
        print("\nTroubleshooting steps:")
        print("1. Verify SMTP server address and port")
        print("2. Check username and password")
        print("3. Make sure TLS is enabled")
        print("4. Check if the AlwaysData email service is activated")
        print("5. Try using the webmail interface to send a test email")

if __name__ == "__main__":
    test_email_connection() 