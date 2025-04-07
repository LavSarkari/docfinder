from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Avg, Count
from doctors.models import Doctor, Specialization
from django.core.paginator import Paginator

def doctor_search(request):
    query = request.GET.get('q', '')
    specialization = request.GET.get('specialization', '')
    location = request.GET.get('location', '')
    custom_location = request.GET.get('custom_location', '')
    rating = request.GET.get('rating', '')
    
    doctors = Doctor.objects.filter(verified=True)
    
    if query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(qualification__icontains=query)
        )
    
    if specialization:
        doctors = doctors.filter(specializations__slug=specialization)
    
    # Use either the selected location or custom location from geolocation
    search_location = location or custom_location
    if search_location:
        doctors = doctors.filter(
            Q(clinic_city__icontains=search_location) |
            Q(clinic_state__icontains=search_location)
        )
    
    if rating:
        doctors = doctors.annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__gte=float(rating))
    
    # Add pagination
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    specializations = Specialization.objects.all()
    
    # List of predefined locations
    locations = [
        'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 
        'Hyderabad', 'Pune', 'Ahmedabad', 'Lucknow', 'Gorakhpur', 
        'Jaipur', 'Chandigarh', 'Kochi', 'Bhopal', 'Indore'
    ]
    
    return render(request, 'search/results.html', {
        'doctors': page_obj,
        'specializations': specializations,
        'locations': locations,
        'query': query,
        'selected_specialization': specialization,
        'selected_location': location,
        'selected_rating': rating
    })

def specialization_search(request, slug):
    specialization = get_object_or_404(Specialization, slug=slug)
    doctors = Doctor.objects.filter(
        specializations=specialization,
        verified=True
    ).annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')
    
    # Add pagination
    paginator = Paginator(doctors, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'search/specialization.html', {
        'specialization': specialization,
        'doctors': page_obj
    })

def global_search(request):
    query = request.GET.get('q', '')
    
    if not query:
        return render(request, 'search/global_results.html', {
            'query': query,
            'doctors': [],
            'specializations': [],
            'locations': []
        })
    
    # Search for doctors
    doctors = Doctor.objects.filter(
        verified=True
    ).filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query) |
        Q(specializations__name__icontains=query) |
        Q(qualification__icontains=query) |
        Q(clinic_address__icontains=query) |
        Q(clinic_city__icontains=query) |
        Q(clinic_state__icontains=query) |
        Q(bio__icontains=query)
    ).distinct()
    
    # Search for specializations
    specializations = Specialization.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
    
    # Find matching locations - collect from doctor records
    locations = Doctor.objects.filter(
        Q(clinic_city__icontains=query) |
        Q(clinic_state__icontains=query)
    ).values('clinic_city', 'clinic_state').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Paginate the results
    doctor_paginator = Paginator(doctors, 5)
    page_number = request.GET.get('page')
    doctor_page = doctor_paginator.get_page(page_number)
    
    spec_paginator = Paginator(specializations, 5)
    spec_page = spec_paginator.get_page(page_number)
    
    return render(request, 'search/global_results.html', {
        'query': query,
        'doctors': doctor_page,
        'specializations': spec_page,
        'locations': locations,
        'doctor_count': doctors.count(),
        'specialization_count': specializations.count(),
        'location_count': locations.count()
    })
