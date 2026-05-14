from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Book, Category
from .models import IssueBook


@login_required
def borrow_books(request):
    books = Book.objects.filter(
        available__gt=0
    )

    categories = Category.objects.all()

    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        books = books.filter(
            title__icontains=query
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

        already_pending = IssueBook.objects.filter(
            user=request.user,
            book=book,
            status='pending'
        ).exists()

        already_approved = IssueBook.objects.filter(
            user=request.user,
            book=book,
            status='approved'
        ).exists()

        if not already_pending and not already_approved:
            IssueBook.objects.create(
                user=request.user,
                book=book
            )

        return redirect('/issue/borrow/')

    return render(
        request,
        'issue/borrow_books.html',
        {
            'books': books,
            'categories': categories
        }
    )


@login_required
def return_books(request):
    borrowed = IssueBook.objects.filter(
        user=request.user,
        status='approved'
    )

    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')

        record = get_object_or_404(
            IssueBook,
            id=issue_id,
            user=request.user
        )

        record.status = 'returned'
        record.save()

        record.book.available += 1
        record.book.save()

        return redirect('/issue/return/')

    return render(
        request,
        'issue/return_books.html',
        {
            'borrowed': borrowed
        }
    )