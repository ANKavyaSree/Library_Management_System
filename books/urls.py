from django.urls import path
from . import views

urlpatterns = [
    path('category/add/', views.add_category, name='add_category'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:id>/', views.edit_book, name='edit_book'),
    path('search/', views.search_book, name='search_book'),
    path('details/<int:id>/', views.book_details, name='book_details'),
]