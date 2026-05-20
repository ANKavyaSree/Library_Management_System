from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from books.models import Book

from books.models import Category

from issue.models import IssueBook
from fines.models import Fine


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

        issue_id = request.POST.get(
            'issue_id'
        )

        return_type = request.POST.get(
            'return_type'
        )

        reason = request.POST.get(
            'reason'
        )

        issue = get_object_or_404(
             IssueBook,
              id=issue_id,
              user=request.user
           )

        # ======================================
        # NORMAL RETURN
        # ======================================

        if return_type == 'normal':

            issue.status = 'returned'

            issue.return_reason = reason

            issue.save()

            # UPDATE AVAILABLE BOOKS

            book = issue.book

            book.available += 1

            book.save()

        # ======================================
        # DAMAGED BOOK
        # ======================================

        elif return_type == 'damaged':

            issue.status = 'damaged'

            issue.return_reason = reason

            issue.save()

            # CREATE DAMAGE FINE

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

            # CREATE LOST BOOK FINE

            Fine.objects.get_or_create(

                user=request.user,

                reason=f"Lost Book: {issue.book.title}",

                defaults={
                    'amount': issue.book.price + 500
                }
            )

        messages.success(
            request,
            'Book return submitted successfully'
        )

        return redirect(
            'teacher_return_books'
        )

    return render(
        request,
        'issue/return_books.html',
        {
            'borrowed': borrowed
        }
    )
@login_required
def teacher_fines(request):

    fines = Fine.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total_fine = fines.filter(
        paid=False
    )

    return render(
        request,
        'fines/my_fines.html',
        {
            'fines': fines,
            'total_fine': total_fine
        }
    )