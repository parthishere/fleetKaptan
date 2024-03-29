"""
URL configuration for fleetKaptan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from rfid.views import list_esps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('schema/', get_schema_view(
        title="API",
        description="API for the Attendace App",
        version="1.0.0"
    ), name="social-schema"),
    path('api/', include_docs_urls(
        title="API",
        description="API for the Attendace App",
    ), name="social-docs"),
    
    # path('api/auth/', include('dj_rest_auth.urls')),
    path("", list_esps),
    path("rfid/", include("rfid.urls", namespace="rfid")),
    path("api/rfid/", include("rfid.api.urls")),
    # path("api//", include("recognizer.api.urls")),
]
