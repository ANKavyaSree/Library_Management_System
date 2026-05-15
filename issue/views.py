from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from books.models import Book, Category
from .models import IssueBook
from rest_framework.decorators import (api_view,permission_classes)
from rest_framework.permissions import (IsAuthenticated)
from rest_framework.response import Response
from rest_framework import status
from .serializers import IssueBookSerializer
from datetime import date, timedelta
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

# =========================================
# REQUEST BOOK API
# =========================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_book_api(request):
    book_id = request.data.get('book')
    if not book_id:
        return Response(
            {
                'message': 'Book ID is required'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    book = get_object_or_404(
        Book,
        id=book_id
    )
    # Check stock
    if book.available <= 0:
        return Response(
            {
                'message': 'Book not available'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    # Prevent duplicate requests
    already_requested = IssueBook.objects.filter(
        user=request.user,
        book=book,
        status__in=['pending', 'approved']
    ).exists()
    if already_requested:
        return Response(
            {
                'message': 'Book already requested'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    issue = IssueBook.objects.create(
        user=request.user,
        book=book
    )
    serializer = IssueBookSerializer(issue)
    return Response(
        {
            'message': 'Book request submitted',
            'data': serializer.data
        },
        status=status.HTTP_201_CREATED
    )
# =========================================
# MY REQUESTS API
# =========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_requests_api(request):
    requests = IssueBook.objects.filter(
        user=request.user
    ).order_by('-request_date')
    serializer = IssueBookSerializer(
        requests,
        many=True
    )
    return Response(serializer.data)
# =========================================
# RETURN BOOK API
# =========================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def return_book_api(request, pk):
    issue = get_object_or_404(
        IssueBook,
        id=pk,
        user=request.user,
        status='approved'
    )
    issue.status = 'returned'
    issue.save()
    # Update stock
    book = issue.book
    book.available += 1
    book.save()
    return Response(
        {
            'message': 'Book returned successfully'
        }
    )
# =========================================
# LIBRARIAN - PENDING REQUESTS
# =========================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_requests_api(request):
    requests = IssueBook.objects.filter(
        status='pending'
    ).order_by('-request_date')
    serializer = IssueBookSerializer(
        requests,
        many=True
    )
    return Response(serializer.data)
# =========================================
# APPROVE REQUEST API
# =========================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_request_api(request, pk):
    issue = get_object_or_404(
        IssueBook,
        id=pk,
        status='pending'
    )
    # Check stock again
    if issue.book.available <= 0:
        return Response(
            {
                'message': 'Book out of stock'
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    # Due date logic
    if issue.user.role == 'teacher':
        days = 15
    else:
        days = 7
    issue.status = 'approved'
    issue.issue_date = date.today()
    issue.due_date = date.today() + timedelta(days=days)
    issue.save()
    # Reduce stock
    book = issue.book
    book.available -= 1
    book.save()
    return Response(
        {
            'message': 'Request approved successfully'
        }
    )
# =========================================
# REJECT REQUEST API
# =========================================
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_request_api(request, pk):
    issue = get_object_or_404(
        IssueBook,
        id=pk,
        status='pending'
    )
    issue.status = 'rejected'
    issue.save()
    return Response(
        {
            'message': 'Request rejected successfully'
        }
    )