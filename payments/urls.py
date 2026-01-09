from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('invoices/', views.invoices_list, name='invoices_list'),
    path('invoices/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('payments/', views.payments_list, name='payments_list'),
    path('pay/<int:invoice_id>/', views.pay_invoice, name='pay_invoice'),
]