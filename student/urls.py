from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard, name='student_dashboard' ),
    path('borrow/',views.borrow_books,name='borrow_books' ),
    path('return/',views.return_books,name='return_books' ),
]