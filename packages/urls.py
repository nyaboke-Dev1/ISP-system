from django.urls import path
from . import views

app_name = 'packages'

urlpatterns = [
    path('', views.plans_list, name='plans_list'),
    # path('<int:plan_id>/', views.plan_detail, name='plan_detail'),
]