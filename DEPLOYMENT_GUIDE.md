# DoctorFinder Deployment Guide for AlwaysData

This guide will walk you through deploying the DoctorFinder application on AlwaysData hosting.

## Prerequisites

1. An AlwaysData account
2. SSH/SFTP client (e.g., FileZilla, WinSCP)
3. Basic knowledge of terminal commands

## Step 1: Set Up Your AlwaysData Account

1. Create an account at [AlwaysData](https://www.alwaysdata.com) if you haven't already
2. Log in to your AlwaysData admin panel

## Step 2: Create a PostgreSQL Database

1. Go to **Databases** in the admin panel
2. Click **Add a database**
3. Choose **PostgreSQL**
4. Set the database name to `lavsarkari_docfinder`
5. Note your database credentials:
   - Host: postgresql-lavsarkari.alwaysdata.net
   - Username: lavsarkari
   - Password: DataBase0808
   - Database name: lavsarkari_docfinder

## Step 3: Configure Email

DoctorFinder uses email for user registration confirmation, password reset, and notifications. AlwaysData provides email services that you'll need to configure:

1. Email credentials:
   - IMAP server: imap-lavsarkari.alwaysdata.net
   - POP server: pop-lavsarkari.alwaysdata.net
   - SMTP server: smtp-lavsarkari.alwaysdata.net
   - Username: lavsarkari@alwaysdata.net
   - Password: DataBase0808
   - Webmail access: [AlwaysData Webmail](https://webmail.alwaysdata.com/) (Roundcube)

2. The email settings in `production_settings.py` have been configured to use these credentials. Make sure these settings are correct:
   ```python
   EMAIL_HOST = 'smtp-lavsarkari.alwaysdata.net'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'lavsarkari@alwaysdata.net'
   EMAIL_HOST_PASSWORD = 'DataBase0808'
   DEFAULT_FROM_EMAIL = 'lavsarkari@alwaysdata.net'
   ADMIN_EMAIL = 'lavsarkari@alwaysdata.net'
   ```

## Step 4: Configure a Python Web Application

1. Go to **Web > Sites** in the admin panel
2. Click **Add a site**
3. Configure the site:
   - Type: **Python WSGI**
   - Address: Your domain (e.g., lavsarkari.alwaysdata.net)
   - Path: /
   - Python version: Select **Python 3.11**
   - Working directory: /home/lavsarkari/www/doctorfinder
   - WSGI application: /home/lavsarkari/www/doctorfinder/wsgi.py
4. Click **Add**

## Step 5: Upload Project Files

### Using SFTP:

1. Connect to your AlwaysData account using SFTP:
   - Host: sftp://lavsarkari.alwaysdata.net
   - Username: lavsarkari
   - Password: Your AlwaysData password
   - Port: 22

2. Create a directory structure:
   ```
   /home/lavsarkari/www/doctorfinder/
   ```

3. Upload all project files to this directory, maintaining the directory structure

### Using SSH:

1. Connect to your AlwaysData account using SSH:
   ```bash
   ssh lavsarkari@ssh-lavsarkari.alwaysdata.net
   ```

2. Create the necessary directories:
   ```bash
   mkdir -p ~/www/doctorfinder
   ```

3. You can also clone from Git if your project is in a repository:
   ```bash
   cd ~/www/doctorfinder
   git clone https://github.com/yourusername/doctorfinder.git .
   ```

## Step 6: Run Deployment Script

After uploading all files to the server, connect via SSH and run:

```bash
cd ~/www/doctorfinder
python deploy.py
```

This will:
1. Install required dependencies
2. Generate a secure secret key
3. Update settings for production
4. Run database migrations
5. Collect static files
6. Create a superuser account

## Step 7: Configure Files and Permissions

Make sure critical files have the right permissions:

```bash
chmod +x ~/www/doctorfinder/deploy.py
chmod +x ~/www/doctorfinder/wsgi.py
chmod -R 755 ~/www/doctorfinder/staticfiles
chmod -R 755 ~/www/doctorfinder/media
```

## Step 8: Testing Your Deployment

1. Visit your site at `https://lavsarkari.alwaysdata.net`
2. Test the email functionality:
   - Register a new user account
   - Try the password reset functionality
   - Check the sent emails in the AlwaysData webmail interface
3. If you encounter any issues, check the AlwaysData logs:
   - Go to **Logs > Access** and **Logs > Error** in the admin panel

## Troubleshooting Common Issues

### Static Files Not Loading

If static files aren't loading, ensure:
- You've run `python manage.py collectstatic`
- The `STATIC_ROOT` path in settings is correct: `/home/lavsarkari/www/doctorfinder/staticfiles`
- Permissions on the static directory are correct

### Email Issues

If emails aren't being sent:
- Verify email credentials in the settings file
- Check if the SMTP server is accessible
- Check spam folders
- Test sending a manual email through webmail to verify the account is working
- Temporarily set `EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'` to see emails in the console logs

### Database Connection Issues

If you're having database issues:
- Verify database credentials in the settings file
- Check if the database server is accessible from your application
- Ensure you've run migrations with `python manage.py migrate`

### Application Errors

If your application returns errors:
- Check the error logs in the AlwaysData admin panel
- Temporarily set `DEBUG = True` in settings to see detailed error pages
- Ensure all dependencies are installed with `pip install --user -r requirements.txt`

## Updating Your Application

To update your application after making changes:

1. Upload the changed files via SFTP
2. Connect via SSH and run:
   ```bash
   cd ~/www/doctorfinder
   python manage.py migrate  # If you've changed models
   python manage.py collectstatic --noinput  # If you've changed static files
   ```

3. Restart the application in the AlwaysData admin panel:
   - Go to **Web > Sites**
   - Select your site and click **Restart** 