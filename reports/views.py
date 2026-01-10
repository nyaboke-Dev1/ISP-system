from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils import timezone

# from .models import UsageRecord  # If you have this model


@login_required
def usage_report(request):
    """View usage statistics"""
    user = request.user

    # Get date range (default to current month)
    today = timezone.now().date()
    first_day = today.replace(day=1)

    # Uncomment if you have UsageRecord model:
    # usage_records = user.usage_records.filter(
    #     date__gte=first_day,
    #     date__lte=today
    # ).order_by('-date')

    # totals = usage_records.aggregate(
    #     total_download=Sum('download_bytes'),
    #     total_upload=Sum('upload_bytes')
    # )

    # total_download_gb = (totals['total_download'] or 0) / (1024**3)
    # total_upload_gb = (totals['total_upload'] or 0) / (1024**3)
    # total_gb = total_download_gb + total_upload_gb

    # For now, use dummy data:
    usage_records = []
    total_download_gb = 0
    total_upload_gb = 0
    total_gb = 0

    # Get active subscription for data cap
    active_subscription = user.subscriptions.filter(status="active").first()

    context = {
        "usage_records": usage_records,
        "total_download_gb": round(total_download_gb, 2),
        "total_upload_gb": round(total_upload_gb, 2),
        "total_gb": round(total_gb, 2),
        "subscription": active_subscription,
    }

    return render(request, "reports/usage.html", context)


@login_required
def export_usage(request):
    """Export usage data as CSV"""
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="usage_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Date", "Download (GB)", "Upload (GB)", "Total (GB)"])

    # Add your data here
    # for record in usage_records:
    #     writer.writerow([record.date, record.download_gb, record.upload_gb, record.total_gb])

    return response
