from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import home

urlpatterns = [

    # HOME PAGE

    path(
        '',
        home,
        name='home'
    ),

    # ADMIN

    path(
        'admin/',
        admin.site.urls
    ),

    # ACCOUNTS

    path(
        '',
        include('accounts.urls')
    ),

    # BOOKS HTML URLs

    path(
        'books/',
        include('books.urls')
    ),

    # BOOKS APIs

    path(
        'api/',
        include('books.urls')
    ),

    # STUDENT

    path(
        'student/',
        include('student.urls')
    ),

    # FINES

    path(
        'fines/',
        include('fines.urls')
    ),

    path(
        'api/',
        include('fines.urls')
    ),

    # TEACHER

    path(
        'teacher/',
        include('teacher.urls')
    ),

    # ISSUE

    path(
        'issue/',
        include('issue.urls')
    ),

    path(
        'api/',
        include('issue.urls')
    ),

    # LIBRARIAN

    path(
        'librarian/',
        include('librarian.urls')
    ),

    path(
        'api/',
        include('librarian.urls')
    ),

]


if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )