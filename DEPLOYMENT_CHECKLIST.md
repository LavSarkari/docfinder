# DoctorFinder Deployment Checklist

Use this checklist to ensure you've completed all necessary steps for deploying to AlwaysData:

## Before Uploading Files

- [ ] Set DEBUG = False in production settings
- [ ] Configure ALLOWED_HOSTS with proper domains
- [ ] Set up database settings for PostgreSQL
- [ ] Configure proper static and media file paths
- [ ] Configure email settings for AlwaysData
- [ ] Enable security settings (HTTPS, secure cookies, etc.)
- [ ] Generate a unique SECRET_KEY
- [ ] Create requirements.txt with all dependencies
- [ ] Test the application locally with production settings

## AlwaysData Setup

- [ ] Create AlwaysData account
- [ ] Set up PostgreSQL database (lavsarkari_docfinder)
- [ ] Configure email service
- [ ] Configure a Python WSGI site
- [ ] Set up working directory and WSGI application path

## File Upload

- [ ] Create necessary directories on server
- [ ] Upload all project files (excluding venv, .git, etc.)
- [ ] Ensure proper file permissions
- [ ] Upload production_settings.py and wsgi.py

## Deployment Steps

- [ ] Run deploy.py script
- [ ] Install dependencies
- [ ] Run database migrations
- [ ] Collect static files
- [ ] Create superuser account
- [ ] Test the site functionality

## Post-Deployment

- [ ] Verify static files are loading correctly
- [ ] Test user registration and login
- [ ] Verify doctor profiles and search functionality
- [ ] Test review submission
- [ ] Test email functionality (registration, password reset)
- [ ] Check admin interface
- [ ] Test on mobile devices
- [ ] Set up SSL certificate (if needed)

## Important Paths

- Working directory: /home/lavsarkari/www/doctorfinder
- WSGI application: /home/lavsarkari/www/doctorfinder/wsgi.py
- Static files: /home/lavsarkari/www/doctorfinder/staticfiles
- Media files: /home/lavsarkari/www/doctorfinder/media

## Database Information

- Host: postgresql-lavsarkari.alwaysdata.net
- Username: lavsarkari
- Password: DataBase0808
- Database name: lavsarkari_docfinder

## Email Information

- IMAP server: imap-lavsarkari.alwaysdata.net
- POP server: pop-lavsarkari.alwaysdata.net
- SMTP server: smtp-lavsarkari.alwaysdata.net
- Username: lavsarkari@alwaysdata.net
- Password: DataBase0808
- Webmail: https://webmail.alwaysdata.com/ (Roundcube)

## Access URLs

- Website: https://lavsarkari.alwaysdata.net
- Admin panel: https://lavsarkari.alwaysdata.net/admin/
- Webmail: https://webmail.alwaysdata.com/

## Troubleshooting Resources

- AlwaysData documentation: https://help.alwaysdata.com/
- Django deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/
- Application logs: Check in AlwaysData admin panel under Logs 