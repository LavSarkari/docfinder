# DoctorFinder - India's Premier Doctor Search Platform

DoctorFinder is a comprehensive platform designed to help people across India find the best healthcare professionals in their area. The platform provides detailed information about doctors, their specializations, qualifications, experience, ratings, and reviews to help users make informed decisions about their healthcare.

## Features

- **Advanced Doctor Search**: Find doctors by specialization, location, and ratings
- **Geolocation Support**: Find doctors near your current location
- **Detailed Doctor Profiles**: View comprehensive profiles with qualifications, experience, and education
- **Review System**: Read and submit verified patient reviews and ratings
- **Doctor Dashboard**: Doctors can manage their profiles and view patient reviews
- **Admin Panel**: Manage doctors, specializations, users, and site content
- **Team Management**: Admin can edit the team section from the admin panel
- **Mobile Responsive**: Fully responsive design for all screen sizes
- **SEO Optimized**: Structured for search engine visibility

## Technology Stack

- Django 5.0.2
- Python 3.11+
- Bootstrap 5
- JavaScript
- HTML5/CSS3
- SQLite (development) / PostgreSQL (production)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/doctorfinder.git
cd doctorfinder
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Collect static files:
```bash
python manage.py collectstatic
```

8. Run the development server:
```bash
python manage.py runserver
```

9. Access the site at http://127.0.0.1:8000/

## Admin Access

The application includes a comprehensive admin interface with the following capabilities:

- **Superuser Access**: Full control over all site functionality
- **Doctor Management**: Approve and verify doctor profiles
- **Content Management**: Edit about page, team members, and contact information
- **User Management**: Manage user accounts and permissions

Admin credentials:
- URL: http://127.0.0.1:8000/admin/
- Username: Set during superuser creation

## Project Structure

- `doctors/` - Doctor profiles, specializations, and doctor dashboard
- `users/` - User authentication, profiles, and permissions
- `reviews/` - Review and rating system for doctors
- `search/` - Advanced search functionality with geolocation
- `pages/` - Static pages (about, contact) and team management
- `static/` - Static files (CSS, JS, images)
- `templates/` - HTML templates
- `media/` - User-uploaded content (profile pictures, etc.)

## Custom Management Commands

The project includes several custom management commands for admin tasks:

- `python count_admins.py` - Display a list of admin users and their permissions
- `python create_superuser.py` - Create a predefined superuser account
- `python create_admin_staff.py` - Create AdminStaff records for superusers

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Developer

Developed by Lav Sarkari
- Email: luv.sarkari@gmail.com