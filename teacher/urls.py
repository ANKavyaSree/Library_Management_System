from django.urls import path
from . import views

urlpatterns = [

    path(
        'dashboard/',
        views.teacher_dashboard,
        name='teacher_dashboard'
    ),

    path(
        'books/',
        views.teacher_books,
        name='teacher_books'
    ),

    path(
        'borrow/<int:book_id>/',
        views.borrow_book,
        name='teacher_borrow_book'
    ),

    path(
        'issued-books/',
        views.teacher_issued_books,
        name='teacher_issued_books'
    ),

    path(
        'return-book/<int:pk>/',
        views.return_book,
        name='teacher_return_book'
    ),
]