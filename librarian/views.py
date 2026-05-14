from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta

from issue.models import IssueBook
from books.models import Book
from fines.models import Fine


@login_required
def dashboard(request):
    total_books = Book.objects.count()
    pending_count = IssueBook.objects.filter(
        status='pending'
    ).count()
    issued_count = IssueBook.objects.filter(
        status='approved'
    ).count()
    unpaid_fines = Fine.objects.filter(
        paid=False
    )
    total_fines = sum(f.amount for f in unpaid_fines)
    return render(
        request,
        'librarian/dashboard.html',
        {
            'total_books': total_books,
            'pending_count': pending_count,
            'issued_count': issued_count,
            'total_fines': total_fines
        }
    )
@login_required
def pending_requests(request):
    requests = IssueBook.objects.filter(
        status='pending'
    ).order_by('-id')
    return render(
        request,
        'librarian/pending_requests.html',
        {
            'requests': requests
        }
    )
@login_required
def approve_request(request, issue_id):
    record = get_object_or_404(
        IssueBook,
        id=issue_id
    )
    if record.user.role == 'teacher':
        days = 15
    else:
        days = 7
    record.status = 'approved'
    record.issue_date = date.today()
    record.due_date = date.today() + timedelta(days=days)
    record.save()
    record.book.available -= 1
    record.book.save()
    return redirect('/librarian/pending/')
@login_required
def reject_request(request, issue_id):
    record = get_object_or_404(
        IssueBook,
        id=issue_id
    )
    record.status = 'rejected'
    record.save()
    return redirect('/librarian/pending/')