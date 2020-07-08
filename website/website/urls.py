"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.views.generic.base import TemplateView
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_file"),
    path('', include('home.urls')),
    path('brexit/', include('brexit.urls')),
    path('excellingyourself/', include('excellingyourself.urls')),
    path('legal/privacypolicy/',TemplateView.as_view(template_name='legal/privacypolicy/index.html')),
    path('legal/cookies/',TemplateView.as_view(template_name='legal/cookies/index.html'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

