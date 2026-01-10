from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from django.db.models import Sum, Q
from django.utils import timezone
from datetime import timedelta
from .forms import SupportTicketForm
from django.contrib.auth import authenticate, login

from accounts.models import SupportTicket
from .forms import CustomerSignUpForm, UserProfileForm

# from .models import SupportTicket  # Uncomment if you have this model


# Public Views
def signup(request):
    """Customer registration"""
    if request.method == "POST":
        form = CustomerSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = "CUSTOMER"  # Set role
            user.save()

            # Auto-login after signup
            login(request, user)
            messages.success(request, "Account created successfully! Welcome!")
            return redirect("accounts:dashboard")
    else:
        form = CustomerSignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


@login_required
def dashboard(request):
    """Customer dashboard"""
    user = request.user

    # Get active subscription
    active_subscription = (
        user.subscriptions.filter(status="active").select_related("package").first()
    )

    # Get recent payments
    recent_payments = user.payments.all().order_by("-timestamp")[:5]

    # Get usage for current month (if you have UsageRecord model)
    today = timezone.now().date()
    first_day = today.replace(day=1)

    # Uncomment if you have usage_records:
    # monthly_usage = user.usage_records.filter(
    #     date__gte=first_day,
    #     date__lte=today
    # ).aggregate(
    #     total_download=Sum('download_bytes'),
    #     total_upload=Sum('upload_bytes')
    # )
    # total_bytes = (monthly_usage['total_download'] or 0) + (monthly_usage['total_upload'] or 0)
    # total_usage_gb = total_bytes / (1024**3)

    # For now, use dummy data:
    total_usage_gb = 0
    data_cap = None
    usage_percentage = 0

    if active_subscription and active_subscription.package.data_cap:
        data_cap = active_subscription.package.data_cap
        if data_cap:
            usage_percentage = (total_usage_gb / data_cap) * 100

    # Get open tickets count (if you have SupportTicket model)
    open_tickets = user.tickets.filter(status__in=["open", "in_progress"]).count()
    open_tickets = 0

    context = {
        "user": user,
        "subscription": active_subscription,
        "recent_payments": recent_payments,
        "total_usage_gb": round(total_usage_gb, 2),
        "data_cap": data_cap,
        "usage_percentage": round(usage_percentage, 1),
        "open_tickets": open_tickets,
    }

    return render(request, "accounts/dashboard.html", context)


@login_required
def profile(request):
    """Customer profile management"""
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("accounts:profile")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})


# Add these if you have SupportTicket model:
@login_required
def tickets(request):
    """View support tickets"""
    # Allow superusers to view all tickets, regular users only their own
    if request.user.is_superuser:
        all_tickets = SupportTicket.objects.all().order_by("-created_at")
    else:
        all_tickets = request.user.tickets.all().order_by("-created_at")
    return render(request, "accounts/tickets/list.html", {"tickets": all_tickets})


@login_required
def ticket_detail(request, ticket_id):
    """View ticket details"""
    # Allow superusers to view all tickets, regular users only their own
    if request.user.is_superuser:
        ticket = get_object_or_404(SupportTicket, id=ticket_id)
    else:
        ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    return render(request, "accounts/tickets/detail.html", {"ticket": ticket})


@login_required
def create_ticket(request):
    """Create new support ticket"""
    if request.method == "POST":
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, f"Support ticket {ticket.ticket_number} created!")
            return redirect("accounts:ticket_detail", ticket_id=ticket.id)
    else:
        form = SupportTicketForm()
    return render(request, "accounts/create_ticket.html", {"form": form})
