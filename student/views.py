from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
from books.models import Book, Category
from .models import BorrowBook, Fine


@login_required
def dashboard(request):
    total_borrowed = BorrowBook.objects.filter(
        student=request.user,
        returned=False
    ).count()

    total_fine = Fine.objects.filter(
        student=request.user,
        paid=False
    )

    fine_amount = sum(f.amount for f in total_fine)

    return render(request, 'student/dashboard.html', {
        'total_borrowed': total_borrowed,
        'fine_amount': fine_amount
    })


@login_required
def borrow_books(request):
    books = Book.objects.filter(available__gt=0)
    categories = Category.objects.all()

    query = request.GET.get('q')
    category = request.GET.get('category')

    if query:
        books = books.filter(title__icontains=query)

    if category:
        books = books.filter(category_id=category)

    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        BorrowBook.objects.create(
            student=request.user,
            book=book,
            due_date=date.today() + timedelta(days=7)
        )

        book.available -= 1
        book.save()

        return redirect('borrow_books')

    return render(request, 'student/borrow_books.html', {
        'books': books,
        'categories': categories
    })


@login_required
def return_books(request):
    borrowed = BorrowBook.objects.filter(
        student=request.user,
        returned=False
    )

    if request.method == 'POST':
        borrow_id = request.POST.get('borrow_id')
        record = get_object_or_404(BorrowBook, id=borrow_id)

        record.returned = True
        record.save()

        record.book.available += 1
        record.book.save()

        if date.today() > record.due_date:
            late_days = (date.today() - record.due_date).days
            Fine.objects.create(
                student=request.user,
                borrow=record,
                amount=late_days * 5
            )

        return redirect('return_books')

    return render(request, 'student/return_books.html', {
        'borrowed': borrowed
    })
@login_required
def fines(request):
    fines = Fine.objects.filter(student=request.user)

    return render(request, 'student/fines.html', {
        'fines': fines
    })