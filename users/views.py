from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserProfileForm
from doctors.models import Doctor
from reviews.models import Review

User = get_user_model()

# Create your views here.

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # Check if username is already taken by another user
            username = form.cleaned_data['username']
            if username and username != request.user.username and User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken. Please choose another one.')
                return render(request, 'users/profile.html', {'form': form})
            
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('users:user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    # Get user's reviews
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    
    # Get doctor profile if user is a doctor
    doctor = None
    if request.user.is_doctor:
        doctor = Doctor.objects.filter(user=request.user).first()
    
    return render(request, 'users/profile.html', {
        'form': form,
        'reviews': reviews,
        'doctor': doctor
    })

@login_required
def my_reviews(request):
    reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'users/my_reviews.html', {'reviews': reviews})

@login_required
def my_favorites(request):
    # Since the favorites model hasn't been implemented yet, return an empty list
    favorites = []
    return render(request, 'users/my_favorites.html', {'favorites': favorites})