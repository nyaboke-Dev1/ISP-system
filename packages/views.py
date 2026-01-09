from django.shortcuts import render, get_object_or_404
from .models import Package


def plans_list(request):
    """Display all service plans"""
    all_plans = Package.objects.filter(is_active=True)
    
    # Group by type if you have plan_type field
    # home_plans = all_plans.filter(plan_type='home')
    # business_plans = all_plans.filter(plan_type='business')
    # enterprise_plans = all_plans.filter(plan_type='enterprise')
    
    context = {
        'plans': all_plans,
        # 'home_plans': home_plans,
        # 'business_plans': business_plans,
        # 'enterprise_plans': enterprise_plans,
    }
    return render(request, 'packages/plans_list.html', context)


def plan_detail(request, plan_id):
    """Display plan details"""
    plan = get_object_or_404(Package, id=plan_id, is_active=True)
    return render(request, 'packages/plan_detail.html', {'plan': plan})

