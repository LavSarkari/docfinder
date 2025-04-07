from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from .forms import ReviewForm
from doctors.models import Doctor

# Create your views here.

@login_required
def add_review(request, doctor_id):
    doctor = get_object_or_404(Doctor, pk=doctor_id)
    
    # Check if user is a doctor and trying to review themselves
    if hasattr(request.user, 'is_doctor') and request.user.is_doctor:
        try:
            user_doctor = Doctor.objects.get(user=request.user)
            if user_doctor.pk == doctor.pk:
                messages.error(request, 'You cannot review yourself.')
                return redirect('doctors:doctor_detail', pk=doctor_id)
        except Doctor.DoesNotExist:
            pass
    
    # Check if user has already reviewed this doctor
    existing_review = Review.objects.filter(doctor=doctor, user=request.user).first()
    if existing_review:
        messages.warning(request, 'You have already reviewed this doctor.')
        return redirect('doctors:doctor_detail', pk=doctor_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.doctor = doctor
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('doctors:doctor_detail', pk=doctor_id)
    else:
        form = ReviewForm()
    
    return render(request, 'reviews/add_review.html', {
        'form': form,
        'doctor': doctor
    })

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('doctors:doctor_detail', pk=review.doctor.pk)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'reviews/edit_review.html', {
        'form': form,
        'review': review
    })

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    doctor_id = review.doctor.pk
    review.delete()
    messages.success(request, 'Your review has been deleted successfully!')
    return redirect('doctors:doctor_detail', pk=doctor_id)
