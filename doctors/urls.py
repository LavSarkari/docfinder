from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctor_home, name='home'),
    path('doctor/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('register/', views.doctor_registration, name='doctor_registration'),
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('specializations/', views.specializations, name='specializations'),
    path('doctor/<int:pk>/book-appointment/', views.book_appointment, name='book_appointment'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
] 