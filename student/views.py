from datetime import date

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from issue.models import IssueBook
from fines.models import Fine

@login_required
def profile(request):

    return render(
        request,
        'student/profile.html'
    )

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
@login_required
def return_books(request):

    borrowed = IssueBook.objects.filter(
        user=request.user,
        status='approved'
    )

    if request.method == 'POST':

        issue_id = request.POST.get('issue_id')

        return_type = request.POST.get('return_type')

        reason = request.POST.get('reason')

        issue = get_object_or_404(
            IssueBook,
            id=issue_id
        )

        # ======================================
        # NORMAL RETURN
        # ======================================

        if return_type == 'normal':

            issue.status = 'return_requested'

            issue.return_reason = reason

            issue.save()

        # ======================================
        # DAMAGED BOOK
        # ======================================

        elif return_type == 'damaged':

            issue.status = 'damaged'

            issue.return_reason = reason

            issue.save()

            Fine.objects.get_or_create(
                user=request.user,
                reason=f"Damaged Book: {issue.book.title}",
                defaults={
                    'amount': issue.book.price + 200
                }
            )

        # ======================================
        # LOST BOOK
        # ======================================

        elif return_type == 'lost':

            issue.status = 'lost'

            issue.return_reason = reason

            issue.save()

            Fine.objects.get_or_create(
                user=request.user,
                reason=f"Lost Book: {issue.book.title}",
                defaults={
                    'amount': issue.book.price + 500
                }
            )

        # ======================================
        # LATE RETURN FINE
        # ONLY FOR STUDENTS
        # ======================================

        if (
            request.user.role == 'student'
            and issue.due_date
            and date.today() > issue.due_date
        ):

            days_late = (
                date.today() - issue.due_date
            ).days

            fine_amount = days_late * 5

            Fine.objects.get_or_create(
                user=request.user,
                reason=f"Late return for {issue.book.title}",
                defaults={
                    'amount': fine_amount
                }
            )

        messages.success(
            request,
            'Return request submitted successfully'
        )

        return redirect('return_books')

    return render(
        request,
        'student/return_books.html',
        {
            'borrowed': borrowed
        }
    )