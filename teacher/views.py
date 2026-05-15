from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from books.models import Book
from issue.models import IssueBook


# ======================================
# TEACHER DASHBOARD
# ======================================
@login_required
def teacher_issued_books(request):

    issues = IssueBook.objects.filter(
        user=request.user
    ).order_by('-request_date')

    return render(
        request,
        'teacher/issued_books.html',
        {'issues': issues}
    )

@login_required
def teacher_dashboard(request):

    context = {

        'total_books': Book.objects.count(),

        'borrowed_books': IssueBook.objects.filter(
            user=request.user,
            status='approved'
        ).count(),

        'pending_requests': IssueBook.objects.filter(
            user=request.user,
            status='pending'
        ).count(),

        'returned_books': IssueBook.objects.filter(
            user=request.user,
            status='returned'
        ).count(),
    }

    return render(
        request,
        'teacher/dashboard.html',
        context
    )


# ======================================
# VIEW ALL BOOKS
# ======================================

@login_required
def teacher_books(request):

    books = Book.objects.all().order_by(
        '-added_on'
    )

    return render(
        request,
        'teacher/books.html',
        {'books': books}
    )


# ======================================
# BORROW BOOK
# ======================================

@login_required
def borrow_book(request, book_id):

    book = get_object_or_404(
        Book,
        id=book_id
    )

    already_requested = IssueBook.objects.filter(
        user=request.user,
        book=book,
        status__in=['pending', 'approved']
    ).exists()

    if not already_requested and book.available > 0:

        IssueBook.objects.create(
            user=request.user,
            book=book,
            status='pending'
        )

    return render(
        request,
        'teacher/request_sent.html'
    )
# ======================================
# RETURN BOOK
# ======================================

@login_required
def return_book(request, pk):

    issue = get_object_or_404(
        IssueBook,
        id=pk,
        user=request.user,
        status='approved'
    )

    issue.status = 'returned'

    issue.save()

    # increase available books

    book = issue.book

    book.available += 1

    book.save()

    return redirect('teacher_issued_books')