from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import Payment
# from .models import Invoice  # If you have Invoice model
from subscriptions.models import Subscription
from .forms import PaymentForm, MpesaPaymentForm


@login_required
def payments_list(request):
    """View payment history"""
    all_payments = request.user.payments.all().order_by('-timestamp')
    
    context = {
        'payments': all_payments,
    }
    
    return render(request, 'payments/payments_list.html', context)


@login_required
def pay_invoice(request, invoice_id):
    """Process payment for subscription/invoice"""
    # This could be invoice_id or subscription_id depending on your setup
    subscription = get_object_or_404(Subscription, id=invoice_id, user=request.user)
    
    if request.method == 'POST':
        form = MpesaPaymentForm(request.POST)
        if form.is_valid():
            # Create payment record
            payment = Payment.objects.create(
                user=request.user,
                subscription=subscription,
                amount=subscription.package.price,
                method='mpesa',
                status='pending'
            )
            
            # Here you would integrate with actual M-Pesa API
            # For now, we'll simulate successful payment
            payment.status = 'completed'
            payment.save()
            
            # Activate subscription
            subscription.is_active = True
            subscription.status = 'active'
            subscription.save()
            
            messages.success(request, 'Payment successful! Your subscription is now active.')
            return redirect('accounts:dashboard')
    else:
        form = MpesaPaymentForm(initial={'amount': subscription.package.price})
    
    context = {
        'form': form,
        'subscription': subscription,
        'amount': subscription.package.price,
    }
    
    return render(request, 'payments/pay_invoice.html', context)


# Uncomment if you have Invoice model:
@login_required
def invoices_list(request):
    """View all invoices"""
    all_invoices = request.user.invoices.all().order_by('-issue_date')
    return render(request, 'payments/invoices_list.html', {'invoices': all_invoices})

@login_required
def invoice_detail(request, invoice_id):
    """View invoice details"""
    invoice = get_object_or_404(Invoice, id=invoice_id, user=request.user)
    payments = invoice.payments.all()
    return render(request, 'payments/invoice_detail.html', {
        'invoice': invoice,
        'payments': payments
    })