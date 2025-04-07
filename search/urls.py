from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.doctor_search, name='doctor_search'),
    path('specialization/<slug:slug>/', views.specialization_search, name='specialization_search'),
    path('global/', views.global_search, name='global_search'),
] 