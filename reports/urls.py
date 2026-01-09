from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('usage/', views.usage_report, name='usage_report'),
    path('usage/export/', views.export_usage, name='export_usage'),
]