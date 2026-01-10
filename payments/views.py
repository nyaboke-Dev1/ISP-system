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
    all_payments = request.user.payments.all().order_by("-timestamp")

    context = {
        "payments": all_payments,
    }

    return render(request, "payments/invoices.html", context)


@login_required
def pay_invoice(request, invoice_id):
    """Process payment for subscription/invoice"""
    # This could be invoice_id or subscription_id depending on your setup
    subscription = get_object_or_404(Subscription, id=invoice_id, user=request.user)

    if request.method == "POST":
        form = MpesaPaymentForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data["phone_number"]

            # Create payment record
            payment = Payment.objects.create(
                user=request.user,
                subscription=subscription,
                amount=subscription.package.price,
                method="mpesa",
                status="pending",
                phone_number=phone_number,
            )

            # Simulate successful payment (for development/testing)
            import time

            time.sleep(2)  # Simulate processing time

            payment.status = "completed"
            payment.mpesa_receipt_number = (
                f'SIM{timezone.now().strftime("%Y%m%d%H%M%S")}'
            )
            payment.transaction_date = timezone.now()
            payment.save()

            # Activate subscription
            subscription.status = "active"
            subscription.save()

            messages.success(
                request, "Payment successful! Your subscription is now active."
            )
            return redirect("accounts:dashboard")
    else:
        form = MpesaPaymentForm(initial={"amount": subscription.package.price})

    context = {
        "form": form,
        "subscription": subscription,
        "amount": subscription.package.price,
    }

    return render(request, "payments/pay_invoice.html", context)


@login_required
def invoices_list(request):
    """View all invoices/payments"""
    all_payments = request.user.payments.all().order_by("-timestamp")
    return render(request, "payments/invoices.html", {"payments": all_payments})
