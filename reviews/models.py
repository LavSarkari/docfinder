from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    doctor = models.ForeignKey('doctors.Doctor', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    verified_visit = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['doctor', 'user']  # One review per doctor per user
        indexes = [
            models.Index(fields=['doctor', 'rating']),
            models.Index(fields=['verified_visit']),
        ]

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.doctor} - {self.rating} stars"
