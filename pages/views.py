from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Avg, Count
from doctors.models import Doctor, Specialization
from .models import TeamMember

# Create your views here.

class AboutView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = TeamMember.objects.all()
        return context

class ContactView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_info'] = {
            'address': 'Grah Enclaves, Chinnat, Lucknow, Uttar Pradesh, India',
            'phone': '+91 7355115183',
            'email': 'luv.sarkari@gmail.com',
            'hours': {
                'weekdays': '9:00 AM - 6:00 PM',
                'saturday': '9:00 AM - 2:00 PM',
                'sunday': 'Closed'
            }
        }
        return context

class PrivacyPolicyView(TemplateView):
    template_name = 'pages/privacy_policy.html'

class TermsOfServiceView(TemplateView):
    template_name = 'pages/terms_of_service.html'

def home_view(request):
    """Home page view."""
    specializations = Specialization.objects.annotate(
        doctor_count=Count('doctors')
    ).order_by('-doctor_count')[:8]
    
    top_doctors = Doctor.objects.filter(verified=True).annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating', '-experience')[:6]
    
    return render(request, 'home.html', {
        'specializations': specializations,
        'top_doctors': top_doctors
    })
