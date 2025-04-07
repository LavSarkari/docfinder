from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('doctors.urls')),
    path('', include('users.urls')),
    path('', include('reviews.urls')),
    path('', include('search.urls')),
    path('', include('pages.urls')),
] 