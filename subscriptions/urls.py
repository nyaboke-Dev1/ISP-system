from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.my_subscription, name='my_subscription'),
    path('subscribe/<int:plan_id>/', views.subscribe, name='subscribe'),
    path('cancel/', views.cancel_subscription, name='cancel'),
    path('upgrade/<int:plan_id>/', views.upgrade_plan, name='upgrade_plan'),
]