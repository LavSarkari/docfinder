from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('reviews/', views.my_reviews, name='my_reviews'),
    path('favorites/', views.my_favorites, name='my_favorites'),
] 