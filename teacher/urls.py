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
        'my-requests/',
        views.teacher_my_requests,
        name='teacher_my_requests'
    ),

    path(
        'return-books/',
        views.teacher_return_books,
        name='teacher_return_books'
    ),
    path(
    'fines/',
    views.teacher_fines,
    name='teacher_fines'
),
]