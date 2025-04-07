from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='team/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Order in which to display this team member")
    
    class Meta:
        ordering = ['order']
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
    
    def __str__(self):
        return self.name

class AdminStaff(models.Model):
    PERMISSION_CHOICES = [
        ('full', 'Full Admin Access'),
        ('doctors', 'Manage Doctors'),
        ('content', 'Manage Content'),
        ('users', 'Manage Users'),
        ('reviews', 'Manage Reviews'),
    ]
    
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='admin_profile')
    role = models.CharField(max_length=100)
    permissions = models.CharField(max_length=20, choices=PERMISSION_CHOICES, default='content')
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='added_admins')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Admin Staff Member"
        verbose_name_plural = "Admin Staff Members"
        
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"
