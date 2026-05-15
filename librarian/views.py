from datetime import date, timedelta
from django.shortcuts import (render,redirect,get_object_or_404)
from django.contrib.auth.decorators import login_required
from books.models import (Book,Category)
from books.forms import (BookForm,CategoryForm)
from issue.models import IssueBook
from fines.models import Fine
from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response
from books.serializers import BookSerializer
from issue.serializers import IssueBookSerializer
from fines.serializers import FineSerializer
# ======================================
# DASHBOARD
# ======================================
@login_required
def dashboard(request):
    context = {
        'total_books': Book.objects.count(),
        'pending_requests': IssueBook.objects.filter(
            status='pending'
        ).count(),
        'issued_books': IssueBook.objects.filter(
            status='approved'
        ).count(),
        'total_fines': Fine.objects.count(),
        'unpaid_fines': Fine.objects.filter(
            paid=False
        ).count(),
    }
    return render(request,'librarian/dashboard.html',context)
# ======================================
# BOOK LIST
# ======================================
@login_required
def book_list(request):
    books = Book.objects.all().order_by('-added_on')
    return render(
        request,
        'librarian/book_list.html',
        {'books': books}
    )
# ======================================
# ADD BOOK
# ======================================
@login_required
def add_book(request):
    form = BookForm(
        request.POST or None
    )
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(
        request,
        'librarian/add_book.html',
        {'form': form}
    )
# ======================================
# EDIT BOOK
# ======================================
@login_required
def edit_book(request, pk):
    book = get_object_or_404(
        Book,
        id=pk
    )
    form = BookForm(
        request.POST or None,
        instance=book
    )
    if form.is_valid():
        form.save()
        return redirect('book_list')
    return render(
        request,
        'librarian/edit_book.html',
        {
            'form': form,
            'book': book
        }
    )
# ======================================
# DELETE BOOK
# ======================================
@login_required
def delete_book(request, pk):
    book = get_object_or_404(
        Book,
        id=pk
    )
    book.delete()
    return redirect('book_list')
# ======================================
# ADD CATEGORY
# ======================================
@login_required
def add_category(request):
    form = CategoryForm(
        request.POST or None
    )
    if form.is_valid():
        form.save()
        return redirect('add_book')
    return render(
        request,
        'librarian/add_category.html',
        {'form': form}
    )
# ======================================
# PENDING REQUESTS
# ======================================
@login_required
def pending_requests(request):
    requests = IssueBook.objects.filter(
        status='pending'
    ).order_by('-request_date')
    return render(
        request,
        'librarian/pending_requests.html',
        {'requests': requests}
    )
# ======================================
# APPROVE REQUEST
# ======================================
@login_required
def approve_request(request, pk):
    issue = get_object_or_404(
        IssueBook,
        id=pk,
        status='pending'
    )
    if issue.book.available > 0:
        if issue.user.role == 'teacher':
            days = 15
        else:
            days = 7
        issue.status = 'approved'
        issue.issue_date = date.today()
        issue.due_date = (
            date.today() + timedelta(days=days)
        )
        issue.save()
        book = issue.book
        book.available -= 1
        book.save()
    return redirect('pending_requests')
# ======================================
# REJECT REQUEST
# ======================================
@login_required
def reject_request(request, pk):
    issue = get_object_or_404(
        IssueBook,
        id=pk,
        status='pending'
    )
    issue.status = 'rejected'
    issue.save()
    return redirect('pending_requests')
# ======================================
# ALL FINES
# ======================================
@login_required
def all_fines(request):
    fines = Fine.objects.all().order_by(
        '-created_at'
    )
    return render(
        request,
        'librarian/all_fines.html',
        {'fines': fines}
    )
# ======================================
# DASHBOARD API
# ======================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_api(request):
    data = {
        'total_books': Book.objects.count(),
        'pending_requests': IssueBook.objects.filter(
            status='pending'
        ).count(),
        'approved_requests': IssueBook.objects.filter(
            status='approved'
        ).count(),
        'returned_books': IssueBook.objects.filter(
            status='returned'
        ).count(),
        'total_fines': Fine.objects.count(),
        'unpaid_fines': Fine.objects.filter(
            paid=False
        ).count(),
    }
    return Response(data)
# ======================================
# ALL BOOKS API
# ======================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_books_api(request):
    books = Book.objects.all()
    serializer = BookSerializer(
        books,
        many=True
    )
    return Response(serializer.data)
# ======================================
# DELETE BOOK API
# ======================================
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book_api(request, pk):
    book = get_object_or_404(
        Book,
        id=pk
    )
    book.delete()
    return Response(
        {
            'message': 'Book deleted successfully'
        }
    )
# ======================================
# PENDING REQUESTS API
# ======================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_requests_api(request):
    requests = IssueBook.objects.filter(
        status='pending'
    )
    serializer = IssueBookSerializer(
        requests,
        many=True
    )
    return Response(serializer.data)
# ======================================
# ALL FINES API
# ======================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_fines_api(request):
    fines = Fine.objects.all()
    serializer = FineSerializer(
        fines,
        many=True
    )
    return Response(serializer.data)