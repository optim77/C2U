# co2_tracker/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tools.urls')),  # Wszystkie API będą dostępne pod /api/
]
