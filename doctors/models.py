from django.db import models
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='bi bi-heart-pulse')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    def doctor_count(self):
        return self.doctors.count()

class Doctor(models.Model):
    EXPERIENCE_CHOICES = [
        ('0-5', '0-5 years'),
        ('5-10', '5-10 years'),
        ('10-15', '10-15 years'),
        ('15+', '15+ years'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    specializations = models.ManyToManyField(Specialization, related_name='doctors')
    registration_number = models.CharField(max_length=50, unique=True)
    qualification = models.CharField(max_length=200)
    experience = models.CharField(max_length=10, choices=EXPERIENCE_CHOICES, default='0-5')
    bio = RichTextField()
    clinic_address = models.TextField()
    clinic_city = models.CharField(max_length=100)
    clinic_state = models.CharField(max_length=100)
    clinic_pincode = models.CharField(max_length=6)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    available_days = models.CharField(max_length=200)  # Store as comma-separated values
    available_hours = models.CharField(max_length=200)  # Store as comma-separated values
    profile_picture = models.ImageField(upload_to='doctors/profile_pics/', blank=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['clinic_city', 'clinic_state']),
            models.Index(fields=['verified']),
        ]

    def __str__(self):
        return f"Dr. {self.user.get_full_name()}"

    def get_absolute_url(self):
        return reverse('doctors:doctor_detail', kwargs={'pk': self.pk})

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return sum(review.rating for review in reviews) / reviews.count()

    @property
    def total_reviews(self):
        return self.reviews.count()

    def get_available_days(self):
        return [day.strip() for day in self.available_days.split(',')]

    def get_available_hours(self):
        return [hour.strip() for hour in self.available_hours.split(',')]

class DoctorDocument(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to='doctors/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.doctor}"
