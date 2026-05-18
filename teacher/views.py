from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

from books.models import Book

from books.models import Category

from issue.models import IssueBook


# =========================================
# DASHBOARD
# =========================================

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


# =========================================
# BORROW BOOKS
# =========================================

@login_required
def teacher_books(request):

    books = Book.objects.all().order_by(
        '-added_on'
    )

    categories = Category.objects.all()

    q = request.GET.get('q')

    category = request.GET.get('category')

    if q:

        books = books.filter(
            title__icontains=q
        )

    if category:

        books = books.filter(
            category_id=category
        )

    if request.method == 'POST':

        book_id = request.POST.get('book_id')

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

            book.available -= 1

            book.save()

        return redirect(
            'teacher_my_requests'
        )

    return render(
        request,
        'issue/borrow_books.html',
        {
            'books': books,
            'categories': categories
        }
    )


# =========================================
# MY REQUESTS
# =========================================

@login_required
def teacher_my_requests(request):

    requests = IssueBook.objects.filter(
        user=request.user
    ).order_by('-request_date')

    return render(
        request,
        'teacher/my_requests.html',
        {
            'requests': requests
        }
    )


# =========================================
# RETURN BOOKS
# =========================================

@login_required
def teacher_return_books(request):

    borrowed = IssueBook.objects.filter(
        user=request.user,
        status='approved'
    )

    if request.method == 'POST':

        borrow_id = request.POST.get(
            'borrow_id'
        )

        issue = get_object_or_404(
            IssueBook,
            id=borrow_id,
            user=request.user
        )

        issue.status = 'returned'

        issue.save()

        book = issue.book

        book.available += 1

        book.save()

        return redirect(
            'teacher_my_requests'
        )

    return render(
        request,
        'issue/return_books.html',
        {
            'borrowed': borrowed
        }
    )