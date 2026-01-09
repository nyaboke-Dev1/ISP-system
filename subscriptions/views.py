from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Subscription
from packages.models import Package


@login_required
def my_subscription(request):
    """View current subscription"""
    # Get all subscriptions
    subscriptions = request.user.subscriptions.all().order_by('-created_at')
    
    # Get active subscription
    active_subscription = subscriptions.filter(is_active=True).first()
    
    # Get available plans for upgrade
    available_plans = Package.objects.filter(is_active=True)
    
    context = {
        'subscriptions': subscriptions,
        'active_subscription': active_subscription,
        'available_plans': available_plans,
    }
    
    return render(request, 'subscriptions/my_subscription.html', context)


@login_required
def subscribe(request, plan_id):
    """Subscribe to a plan"""
    plan = get_object_or_404(Package, id=plan_id, is_active=True)
    
    # Check if user already has active subscription
    has_active = request.user.subscriptions.filter(is_active=True).exists()
    
    if has_active:
        messages.warning(request, 'You already have an active subscription. Please cancel it first.')
        return redirect('subscriptions:my_subscription')
    
    if request.method == 'POST':
        # Create subscription
        subscription = Subscription.objects.create(
            user=request.user,
            package=plan,
            start_date=timezone.now(),
            is_active=False,  # Will be activated after payment
            status='pending'
        )
        
        messages.success(request, f'Subscription to {plan.name} created! Please complete payment.')
        return redirect('payments:pay_invoice', invoice_id=subscription.id)  # Or wherever you handle payment
    
    context = {
        'plan': plan,
    }
    return render(request, 'subscriptions/subscribe.html', context)


@login_required
def upgrade_plan(request, plan_id):
    """Upgrade to a different plan"""
    new_plan = get_object_or_404(Package, id=plan_id, is_active=True)
    
    # Get current active subscription
    current_subscription = request.user.subscriptions.filter(is_active=True).first()
    
    if not current_subscription:
        messages.error(request, 'You need an active subscription first.')
        return redirect('packages:plans_list')
    
    if request.method == 'POST':
        # Cancel current subscription
        current_subscription.is_active = False
        current_subscription.status = 'cancelled'
        current_subscription.save()
        
        # Create new subscription
        new_subscription = Subscription.objects.create(
            user=request.user,
            package=new_plan,
            start_date=timezone.now(),
            is_active=True,
            status='active'
        )
        
        messages.success(request, f'Successfully upgraded to {new_plan.name}!')
        return redirect('subscriptions:my_subscription')
    
    context = {
        'new_plan': new_plan,
        'current_subscription': current_subscription,
    }
    
    return render(request, 'subscriptions/upgrade_plan.html', context)


@login_required
def cancel_subscription(request):
    """Cancel active subscription"""
    active_subscription = request.user.subscriptions.filter(is_active=True).first()
    
    if not active_subscription:
        messages.error(request, 'No active subscription to cancel.')
        return redirect('subscriptions:my_subscription')
    
    if request.method == 'POST':
        active_subscription.is_active = False
        active_subscription.status = 'cancelled'
        active_subscription.save()
        
        messages.success(request, 'Subscription cancelled successfully.')
        return redirect('subscriptions:my_subscription')
    
    return render(request, 'subscriptions/cancel_subscription.html', {
        'subscription': active_subscription
    })