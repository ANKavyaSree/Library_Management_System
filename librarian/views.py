from datetime import date, timedelta

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Sum

from books.models import (
    Book,
    Category
)

from books.forms import (
    BookForm,
    CategoryForm
)

from issue.models import IssueBook

from fines.models import Fine
from fines.forms import FineForm

from accounts.models import CustomUser

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

    total_books = Book.objects.count()

    total_available_books = Book.objects.aggregate(
        total=Sum('available')
    )['total'] or 0

    pending_requests = IssueBook.objects.filter(
        status__in=[
            'pending',
            'return_requested'
        ]
    ).count()

    issued_books = IssueBook.objects.filter(
        status='approved'
    ).count()

    total_fines = Fine.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0

    unpaid_fines = Fine.objects.filter(
        paid=False
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    return render(
        request,
        'librarian/dashboard.html',
        {
            'total_books': total_books,
            'total_available_books': total_available_books,
            'pending_requests': pending_requests,
            'issued_books': issued_books,
            'total_fines': total_fines,
            'unpaid_fines': unpaid_fines,
        }
    )


# ======================================
# BOOK LIST
# ======================================

@login_required
def book_list(request):

    books = Book.objects.all().order_by(
        '-added_on'
    )

    return render(
        request,
        'librarian/book_list.html',
        {
            'books': books
        }
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

        messages.success(
            request,
            'Book added successfully'
        )

        return redirect(
            'book_list'
        )

    return render(
        request,
        'librarian/add_book.html',
        {
            'form': form
        }
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

        messages.success(
            request,
            'Book updated successfully'
        )

        return redirect(
            'book_list'
        )

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

    messages.success(
        request,
        'Book deleted successfully'
    )

    return redirect(
        'book_list'
    )


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

        messages.success(
            request,
            'Category added successfully'
        )

        return redirect(
            'book_list'
        )

    return render(
        request,
        'librarian/add_category.html',
        {
            'form': form
        }
    )


# ======================================
# PENDING REQUESTS
# ======================================

@login_required
def pending_requests(request):

    requests = IssueBook.objects.filter(
        status__in=[
            'pending',
            'return_requested'
        ]
    ).order_by('-request_date')

    return render(
        request,
        'librarian/pending_requests.html',
        {
            'requests': requests
        }
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

            days = 30

        else:

            days = 14

        issue.status = 'approved'

        issue.issue_date = date.today()

        issue.due_date = (
            date.today() + timedelta(days=days)
        )

        issue.save()

        issue.book.available -= 1
        issue.book.save()

        messages.success(
            request,
            'Book request approved successfully'
        )

    else:

        messages.error(
            request,
            'No books available'
        )

    return redirect(
        'pending_requests'
    )


# ======================================
# REJECT REQUEST
# ======================================

@login_required
def reject_request(request, pk):

    issue = get_object_or_404(
        IssueBook,
        pk=pk
    )

    if request.method == 'POST':

        reason = request.POST.get(
            'reason'
        )

        issue.status = 'rejected'

        issue.rejection_reason = reason

        issue.save()

        messages.success(
            request,
            'Request rejected successfully'
        )

        return redirect(
            'pending_requests'
        )

    return render(
        request,
        'librarian/reject_request.html',
        {
            'issue': issue
        }
    )


# ======================================
# RETURNED BOOKS
# ======================================

@login_required
def returned_books(request):

    returned = IssueBook.objects.filter(
        status__in=[
            'returned',
            'damaged',
            'lost'
        ]
    ).order_by('-request_date')

    today = date.today()

    for issue in returned:

        # ======================================
        # STUDENT LATE RETURN FINE
        # ======================================

        if (
            issue.user.role == 'student'
            and issue.status == 'returned'
            and issue.due_date
            and today > issue.due_date
        ):

            days_late = (
                today - issue.due_date
            ).days

            fine_amount = days_late * 5

            Fine.objects.get_or_create(
                user=issue.user,
                reason=f"Late return for {issue.book.title}",
                defaults={
                    'amount': fine_amount,
                    'paid': False
                }
            )

        # ======================================
        # DAMAGED BOOK FINE
        # ======================================

        elif issue.status == 'damaged':

            Fine.objects.get_or_create(
                user=issue.user,
                reason=f"Damaged Book: {issue.book.title}",
                defaults={
                    'amount': issue.book.price + 200,
                    'paid': False
                }
            )

        # ======================================
        # LOST BOOK FINE
        # ======================================

        elif issue.status == 'lost':

            Fine.objects.get_or_create(
                user=issue.user,
                reason=f"Lost Book: {issue.book.title}",
                defaults={
                    'amount': issue.book.price + 500,
                    'paid': False
                }
            )

    return render(
        request,
        'librarian/returned_books.html',
        {
            'returned': returned
        }
    )


# ======================================
# APPROVE RETURN
# ======================================

@login_required
def approve_return(request, pk):

    issue = get_object_or_404(
        IssueBook,
        id=pk
    )

    action = request.POST.get('action')

    # ======================================
    # NORMAL RETURN
    # ======================================

    if action == 'returned':

        issue.status = 'returned'

        issue.save()

        issue.book.available += 1
        issue.book.save()

        # STUDENT LATE FINE ONLY

        if (
            issue.user.role == 'student'
            and issue.due_date
            and date.today() > issue.due_date
        ):

            days_late = (
                date.today() - issue.due_date
            ).days

            fine_amount = days_late * 5

            Fine.objects.get_or_create(
                user=issue.user,
                reason=f"Late return for {issue.book.title}",
                defaults={
                    'amount': fine_amount,
                    'paid': False
                }
            )

    # ======================================
    # DAMAGED BOOK
    # ======================================

    elif action == 'damaged':

        issue.status = 'damaged'
        issue.save()

        Fine.objects.get_or_create(
            user=issue.user,
            reason=f"Damaged Book: {issue.book.title}",
            defaults={
                'amount': issue.book.price + 200,
                'paid': False
            }
        )

    # ======================================
    # LOST BOOK
    # ======================================

    elif action == 'lost':

        issue.status = 'lost'
        issue.save()

        Fine.objects.get_or_create(
            user=issue.user,
            reason=f"Lost Book: {issue.book.title}",
            defaults={
                'amount': issue.book.price + 500,
                'paid': False
            }
        )

    return redirect('returned_books')


# ======================================
# ALL FINES
# ======================================

@login_required
def all_fines(request):

    fines = Fine.objects.all().order_by(
        '-created_at'
    )

    paid_count = fines.filter(
        paid=True
    ).count()

    unpaid_count = fines.filter(
        paid=False
    ).count()

    return render(
        request,
        'librarian/all_fines.html',
        {
            'fines': fines,
            'paid_count': paid_count,
            'unpaid_count': unpaid_count
        }
    )


# ======================================
# ADD FINE
# ======================================

@login_required
def add_fine(request):

    form = FineForm(
        request.POST or None
    )

    if form.is_valid():

        form.save()

        messages.success(
            request,
            'Fine added successfully'
        )

        return redirect(
            'all_fines'
        )

    return render(
        request,
        'librarian/add_fine.html',
        {
            'form': form
        }
    )


# ======================================
# STUDENTS LIST
# ======================================

@login_required
def students_list(request):

    students = CustomUser.objects.filter(
        role='student'
    )

    return render(
        request,
        'librarian/students.html',
        {
            'students': students
        }
    )


# ======================================
# TEACHERS LIST
# ======================================

@login_required
def teachers_list(request):

    teachers = CustomUser.objects.filter(
        role='teacher'
    )

    return render(
        request,
        'librarian/teachers.html',
        {
            'teachers': teachers
        }
    )


# ======================================
# DELETE STUDENT
# ======================================

@login_required
def delete_student(request, pk):

    student = get_object_or_404(
        CustomUser,
        id=pk,
        role='student'
    )

    student.delete()

    return redirect(
        'students_list'
    )


# ======================================
# DELETE TEACHER
# ======================================

@login_required
def delete_teacher(request, pk):

    teacher = get_object_or_404(
        CustomUser,
        id=pk,
        role='teacher'
    )

    teacher.delete()

    return redirect(
        'teachers_list'
    )


# ======================================
# DASHBOARD API
# ======================================

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_api(request):

    data = {

        'total_books': Book.objects.count(),

        'total_available_books': Book.objects.aggregate(
            total=Sum('available')
        )['total'] or 0,

        'pending_requests': IssueBook.objects.filter(
            status__in=[
                'pending',
                'return_requested'
            ]
        ).count(),

        'issued_books': IssueBook.objects.filter(
            status='approved'
        ).count(),

        'total_fines': Fine.objects.aggregate(
            total=Sum('amount')
        )['total'] or 0,

        'unpaid_fines': Fine.objects.filter(
            paid=False
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0,
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
        status__in=[
            'pending',
            'return_requested'
        ]
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