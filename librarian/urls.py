from django.urls import path
from . import views

urlpatterns = [
    # ======================================
    # DASHBOARD
    # ======================================
    path('dashboard/',views.dashboard,name='librarian_dashboard'),
    # ======================================
    # BOOK MANAGEMENT
    # ======================================
    path('books/',views.book_list,name='book_list'),
    path('books/add/',views.add_book,name='add_book'),
    path('books/edit/<int:pk>/',views.edit_book,name='edit_book'),
    path('books/delete/<int:pk>/',views.delete_book,name='delete_book'),
    path('category/add/',views.add_category,name='add_category'),
    # ======================================
    # ISSUE MANAGEMENT
    # ======================================
    path('pending/',views.pending_requests,name='pending_requests'),
    path('approve/<int:pk>/',views.approve_request,name='approve_request'),
    path('reject/<int:pk>/',views.reject_request,name='reject_request'),
    # ======================================
    # FINE MANAGEMENT
    # ======================================
    path('fines/',views.all_fines,name='all_fines'),
    path('librarian/dashboard/',views.dashboard_api),
    path('librarian/books/',views.all_books_api),
    path('librarian/books/delete/<int:pk>/',views.delete_book_api),
    path('librarian/pending/',views.pending_requests_api),
    path('librarian/all-fines/',views.all_fines_api),
]
