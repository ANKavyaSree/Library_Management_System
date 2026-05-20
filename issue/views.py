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
from django.contrib import messages
from issue.models import IssueBook
from fines.models import Fine
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

    # FETCH APPROVED BOOKS

    borrowed = IssueBook.objects.filter(
        user=request.user,
        status='approved'
    )

    # HANDLE RETURN

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
            user=request.user,
            status='approved'
        )

        # =====================================
        # NORMAL RETURN
        # =====================================

        if return_type == 'normal':

            issue.status = 'returned'

            issue.return_reason = ''

            issue.save(
                update_fields=[
                    'status',
                    'return_reason'
                ]
            )

            # INCREASE AVAILABLE BOOKS

            book = issue.book

            book.available += 1

            book.save(
                update_fields=['available']
            )

            # =====================================
            # LATE FINE ONLY FOR STUDENTS
            # =====================================

            if (
                request.user.role == 'student'
                and issue.due_date
                and date.today() > issue.due_date
            ):

                late_days = (
                    date.today() - issue.due_date
                ).days

                fine_amount = late_days * 5

                Fine.objects.create(
                    user=request.user,
                    amount=fine_amount,
                    reason=f"Late Return Fine for {issue.book.title}"
                )

        # =====================================
        # DAMAGED BOOK
        # =====================================

        elif return_type == 'damaged':

            issue.status = 'damaged'

            issue.return_reason = reason

            issue.save(
                update_fields=[
                    'status',
                    'return_reason'
                ]
            )

            # DAMAGE FINE FOR BOTH
            # STUDENT & TEACHER

            Fine.objects.create(
                user=request.user,
                amount=issue.book.price + 200,
                reason=f"Damaged Book : {issue.book.title}"
            )

        # =====================================
        # LOST BOOK
        # =====================================

        elif return_type == 'lost':

            issue.status = 'lost'

            issue.return_reason = reason

            issue.save(
                update_fields=[
                    'status',
                    'return_reason'
                ]
            )

            # LOST BOOK FINE FOR BOTH
            # STUDENT & TEACHER

            Fine.objects.create(
                user=request.user,
                amount=issue.book.price + 500,
                reason=f"Lost Book : {issue.book.title}"
            )

        return redirect(
            '/issue/return/'
        )

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