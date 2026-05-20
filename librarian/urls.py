from django.urls import path

from . import views

urlpatterns = [

    # ======================================
    # DASHBOARD
    # ======================================

    path(
        'dashboard/',
        views.dashboard,
        name='librarian_dashboard'
    ),

    # ======================================
    # BOOK MANAGEMENT
    # ======================================

    path(
        'books/',
        views.book_list,
        name='book_list'
    ),

    path(
        'books/add/',
        views.add_book,
        name='add_book'
    ),

    path(
        'books/edit/<int:pk>/',
        views.edit_book,
        name='edit_book'
    ),

    path(
        'books/delete/<int:pk>/',
        views.delete_book,
        name='delete_book'
    ),

    path(
        'category/add/',
        views.add_category,
        name='add_category'
    ),

    # ======================================
    # ISSUE MANAGEMENT
    # ======================================

    path(
        'pending/',
        views.pending_requests,
        name='pending_requests'
    ),

    path(
        'approve/<int:pk>/',
        views.approve_request,
        name='approve_request'
    ),

    path(
        'reject/<int:pk>/',
        views.reject_request,
        name='reject_request'
    ),

    path(
        'returned/',
        views.returned_books,
        name='returned_books'
    ),

    # ======================================
    # STUDENT MANAGEMENT
    # ======================================

    path(
        'students/',
        views.students_list,
        name='students_list'
    ),
    path(
        'students/delete/<int:pk>/',
        views.delete_student,
        name='delete_student'
    ),

    # ======================================
    # TEACHER MANAGEMENT
    # ======================================

    path(
        'teachers/',
        views.teachers_list,
        name='teachers_list'
    ),



    path(
        'teachers/delete/<int:pk>/',
        views.delete_teacher,
        name='delete_teacher'
    ),

    # ======================================
    # FINE MANAGEMENT
    # ======================================

    path(
        'fines/',
        views.all_fines,
        name='all_fines'
    ),

    path(
    'fines/add/',
    views.add_fine,
    name='add_fine'
),

    # ======================================
    # API ROUTES
    # ======================================

    path(
        'api/dashboard/',
        views.dashboard_api,
        name='dashboard_api'
    ),

    path(
        'api/books/',
        views.all_books_api,
        name='all_books_api'
    ),

    path(
        'api/books/delete/<int:pk>/',
        views.delete_book_api,
        name='delete_book_api'
    ),

    path(
        'api/pending/',
        views.pending_requests_api,
        name='pending_requests_api'
    ),

    path(
        'api/all-fines/',
        views.all_fines_api,
        name='all_fines_api'
    ),
]