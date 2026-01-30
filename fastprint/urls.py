"""
URL configuration for fastprint project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventory.urls')),
]

# Customize admin site
admin.site.site_header = "FastPrint Admin"
admin.site.site_title = "FastPrint Admin Portal"
admin.site.index_title = "Selamat datang di FastPrint Management System"
