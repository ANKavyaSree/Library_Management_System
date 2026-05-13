from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='teacher_dashboard'),
    path('borrow/',views.borrow_books,name='teacher_borrow'),
    path('return/',views.return_books,name='teacher_return'),
]