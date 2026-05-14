from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from issue.models import IssueBook
from fines.models import Fine


@login_required
def dashboard(request):
    total_borrowed = IssueBook.objects.filter(
        user=request.user,
        status='approved'
    ).count()

    pending_requests = IssueBook.objects.filter(
        user=request.user,
        status='pending'
    ).count()

    unpaid_fines = Fine.objects.filter(
        user=request.user,
        paid=False
    )

    fine_amount = sum(f.amount for f in unpaid_fines)

    return render(request, 'student/dashboard.html', {
        'total_borrowed': total_borrowed,
        'pending_requests': pending_requests,
        'fine_amount': fine_amount
    })


@login_required
def my_requests(request):
    requests = IssueBook.objects.filter(
        user=request.user
    ).order_by('-id')

    return render(request, 'student/my_requests.html', {
        'requests': requests
    })