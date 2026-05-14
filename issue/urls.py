from django.urls import path
from . import views

urlpatterns = [
    path('borrow/',views.borrow_books, name='issue_borrow'),
    path('return/',views.return_books,name='issue_return'),
]