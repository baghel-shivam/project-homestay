# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin_you_can_handle_it/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),          # UI Kits Html files
    path("", include("mainapp.urls")) 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)