from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Doctor, Specialization
from .forms import DoctorRegistrationForm, DoctorDocumentForm, DoctorProfileEditForm
from reviews.models import Review
from django import forms

def doctor_home(request):
    specializations = Specialization.objects.annotate(
        doctor_count=Count('doctors')
    ).order_by('-doctor_count')[:8]
    
    top_doctors = Doctor.objects.filter(verified=True).annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:6]
    
    return render(request, 'home.html', {
        'specializations': specializations,
        'top_doctors': top_doctors
    })

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    reviews = Review.objects.filter(doctor=doctor).order_by('-created_at')
    return render(request, 'doctors/doctor_detail.html', {
        'doctor': doctor,
        'reviews': reviews
    })

@login_required
def doctor_registration(request):
    if request.user.is_doctor:
        return redirect('doctors:doctor_dashboard')
    
    if request.method == 'POST':
        form = DoctorRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = request.user
            doctor.save()
            form.save_m2m()  # Save many-to-many relationships
            request.user.is_doctor = True
            request.user.save()
            messages.success(request, 'Your doctor profile has been created successfully!')
            return redirect('doctors:doctor_dashboard')
    else:
        form = DoctorRegistrationForm()
    
    return render(request, 'doctors/doctor_registration.html', {'form': form})

@login_required
def doctor_dashboard(request):
    if not request.user.is_doctor:
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, user=request.user)
    reviews = Review.objects.filter(doctor=doctor).order_by('-created_at')
    documents = doctor.documents.all()
    
    if request.method == 'POST':
        form = DoctorDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.doctor = doctor
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('doctors:doctor_dashboard')
    else:
        form = DoctorDocumentForm()
    
    return render(request, 'doctors/doctor_dashboard.html', {
        'doctor': doctor,
        'reviews': reviews,
        'documents': documents,
        'form': form
    })

@login_required
def book_appointment(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    
    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')
        
        # TODO: Create Appointment model and save the appointment
        # For now, just show a success message
        messages.success(
            request, 
            f'Appointment request sent to Dr. {doctor.user.get_full_name()} for {appointment_date} at {appointment_time}.'
        )
        return redirect('doctors:doctor_detail', pk=doctor.pk)
    
    return redirect('doctors:doctor_detail', pk=doctor.pk)

def specializations(request):
    # Get all specializations with doctor count
    specializations = Specialization.objects.annotate(
        doctor_count=Count('doctors')
    ).order_by('name')
    
    # Get popular specializations (top 4 by doctor count)
    popular_specializations = Specialization.objects.annotate(
        doctor_count=Count('doctors')
    ).order_by('-doctor_count')[:4]
    
    # Add default Bootstrap Icons for specializations
    specialization_icons = {
        'Cardiology': 'bi bi-heart-pulse',
        'Dermatology': 'bi bi-bandaid',
        'Endocrinology': 'bi bi-activity',
        'Gastroenterology': 'bi bi-capsule',
        'General Medicine': 'bi bi-hospital',
        'Neurology': 'bi bi-lightning',
        'Oncology': 'bi bi-shield-plus',
        'Ophthalmology': 'bi bi-eye',
        'Orthopedics': 'bi bi-universal-access',
        'Pediatrics': 'bi bi-emoji-smile',
        'Psychiatry': 'bi bi-person-hearts',
        'Urology': 'bi bi-droplet',
    }
    
    # Add icons to each specialization
    for specialization in specializations:
        specialization.icon = specialization_icons.get(specialization.name, 'bi bi-heart-pulse')
    
    for specialization in popular_specializations:
        specialization.icon = specialization_icons.get(specialization.name, 'bi bi-heart-pulse')
    
    return render(request, 'doctors/specializations.html', {
        'specializations': specializations,
        'popular_specializations': popular_specializations
    })

@login_required
def edit_profile(request):
    if not request.user.is_doctor:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    
    doctor = get_object_or_404(Doctor, user=request.user)
    
    if request.method == 'POST':
        form = DoctorProfileEditForm(request.POST, request.FILES, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('doctors:doctor_dashboard')
    else:
        form = DoctorProfileEditForm(instance=doctor)
    
    return render(request, 'doctors/edit_profile.html', {
        'form': form,
        'doctor': doctor
    })
