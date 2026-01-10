from django.shortcuts import render, get_object_or_404
from .models import Package


def plans_list(request):
    """Display all service plans"""
    all_plans = Package.objects.filter(is_active=True)

    # Check if user has active subscription
    has_active_subscription = False
    if request.user.is_authenticated:
        has_active_subscription = request.user.subscriptions.filter(
            status="active"
        ).exists()

    context = {
        "plans": all_plans,
        "has_active_subscription": has_active_subscription,
    }
    return render(request, "packages/list.html", context)


def plan_detail(request, plan_id):
    """Display plan details"""
    plan = get_object_or_404(Package, id=plan_id, is_active=True)
    return render(request, "packages/detail.html", {"plan": plan})
