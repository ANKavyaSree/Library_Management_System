from django.urls import path
from . import views

urlpatterns = [
    path('category/add/', views.add_category, name='add_category'),
    path('add/', views.add_book, name='add_book'),
    path('edit/<int:id>/', views.edit_book, name='edit_book'),
    path('search/', views.search_book, name='search_book'),
    path('details/<int:id>/', views.book_details, name='book_details'),
    # =========================
    # CATEGORY APIs
    # =========================

    path(
        'categories/',
        views.category_list_api,
        name='category_list_api'
    ),

    path(
        'categories/add/',
        views.add_category_api,
        name='add_category_api'
    ),

    # =========================
    # BOOK APIs
    # =========================

    path(
        'books/',
        views.book_list_api,
        name='book_list_api'
    ),

    path(
        'books/<int:pk>/',
        views.book_detail_api,
        name='book_detail_api'
    ),

    path(
        'books/add_book/',
        views.add_book_api,
        name='add_book_api'
    ),

    path(
        'books/update_book/<int:pk>/',
        views.update_book_api,
        name='update_book_api'
    ),

    path(
        'books/delete_book/<int:pk>/',
        views.delete_book_api,
        name='delete_book_api'
    ),
]
