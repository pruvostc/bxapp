from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    path('referendum/', views.referendum, name='referendum'),
    path('whatisbrexit/', views.whatisbrexit, name='whatisbrexit'),
    path('economic-charts/', views.echarts, name='economic-charts'),
]