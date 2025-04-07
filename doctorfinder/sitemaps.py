from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from doctors.models import Doctor

class DoctorSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Doctor.objects.filter(verified=True)

    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['home', 'about', 'contact', 'privacy_policy', 'terms', 'doctor_search', 'specializations']

    def location(self, item):
        return reverse(item) 