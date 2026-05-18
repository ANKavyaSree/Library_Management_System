from datetime import date, timedelta

from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.contrib.auth.decorators import login_required

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

from accounts.models import CustomUser

from accounts.forms import RegisterForm

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

        'total_fines': Fine.objects.filter(
            user__role='student'
        ).count(),

        'unpaid_fines': Fine.objects.filter(
            user__role='student',
            paid=False
        ).count(),

        'students_count': CustomUser.objects.filter(
            role='student'
        ).count(),

        'teachers_count': CustomUser.objects.filter(
            role='teacher'
        ).count(),
    }

    return render(
        request,
        'librarian/dashboard.html',
        context
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
        status='pending'
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

        # REDUCE AVAILABLE COUNT

        book = issue.book

        book.available -= 1

        book.save()

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
        id=pk,
        status='pending'
    )

    issue.status = 'rejected'

    issue.save()

    return redirect(
        'pending_requests'
    )


# ======================================
# RETURNED BOOKS
# ======================================

@login_required
def returned_books(request):

    returned = IssueBook.objects.filter(
        status='returned'
    ).order_by('-request_date')

    today = date.today()

    for issue in returned:

        if (
            issue.user.role == 'student'
            and issue.due_date
            and today > issue.due_date
        ):

            days_late = (
                today - issue.due_date
            ).days

            fine_amount = days_late * 5

            fine_exists = Fine.objects.filter(
                user=issue.user,
                reason__icontains=issue.book.title
            ).exists()

            if not fine_exists:

                Fine.objects.create(
                    user=issue.user,
                    amount=fine_amount,
                    reason=f"Late return for {issue.book.title}"
                )

    return render(
        request,
        'librarian/returned_books.html',
        {
            'returned': returned
        }
    )


# ======================================
# ALL FINES
# ======================================

@login_required
def all_fines(request):

    fines = Fine.objects.filter(
        user__role='student'
    ).order_by('-created_at')

    return render(
        request,
        'librarian/all_fines.html',
        {
            'fines': fines
        }
    )


# ======================================
# ADD FINE
# ======================================

@login_required
def add_fine(request):

    students = CustomUser.objects.filter(
        role='student'
    )

    if request.method == 'POST':

        user_id = request.POST.get(
            'student'
        )

        amount = request.POST.get(
            'amount'
        )

        reason = request.POST.get(
            'reason'
        )

        student = get_object_or_404(
            CustomUser,
            id=user_id,
            role='student'
        )

        Fine.objects.create(
            user=student,
            amount=amount,
            reason=reason
        )

        return redirect(
            'all_fines'
        )

    return render(
        request,
        'librarian/add_fine.html',
        {
            'students': students
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
# ADD STUDENT
# ======================================

@login_required
def add_student(request):

    form = RegisterForm(
        request.POST or None
    )

    if request.method == 'POST':

        if form.is_valid():

            user = form.save(
                commit=False
            )

            user.role = 'student'

            user.save()

            return redirect(
                'students_list'
            )

    return render(
        request,
        'librarian/add_student.html',
        {
            'form': form
        }
    )


# ======================================
# ADD TEACHER
# ======================================

@login_required
def add_teacher(request):

    form = RegisterForm(
        request.POST or None
    )

    if request.method == 'POST':

        if form.is_valid():

            user = form.save(
                commit=False
            )

            user.role = 'teacher'

            user.save()

            return redirect(
                'teachers_list'
            )

    return render(
        request,
        'librarian/add_teacher.html',
        {
            'form': form
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

        'pending_requests': IssueBook.objects.filter(
            status='pending'
        ).count(),

        'approved_requests': IssueBook.objects.filter(
            status='approved'
        ).count(),

        'returned_books': IssueBook.objects.filter(
            status='returned'
        ).count(),

        'total_fines': Fine.objects.filter(
            user__role='student'
        ).count(),

        'unpaid_fines': Fine.objects.filter(
            user__role='student',
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

    fines = Fine.objects.filter(
        user__role='student'
    )

    serializer = FineSerializer(
        fines,
        many=True
    )

    return Response(serializer.data)