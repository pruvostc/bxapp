from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('vueforum/', views.vueforum, name='forum'),
    path('contact', views.contact, name='contact'),
] + static(settings.FORUM_URL, document_root=settings.FORUM_ROOT)