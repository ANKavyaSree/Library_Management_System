from django.urls import path
from . import views

urlpatterns = [
    path('borrow/',views.borrow_books, name='issue_borrow'),
    path('return/',views.return_books,name='issue_return'),
     # =====================================
    # STUDENT / TEACHER APIs
    # =====================================
    path('issues/request/',views.request_book_api,name='request_book_api'),
    path('issues/my-requests/',views.my_requests_api,name='my_requests_api'),
    path('issues/return/<int:pk>/',views.return_book_api,name='return_book_api'),
    # =====================================
    # LIBRARIAN APIs
    # =====================================
    path('librarian/pending/',views.pending_requests_api,name='pending_requests_api'),
    path('librarian/approve/<int:pk>/',views.approve_request_api,name='approve_request_api'),
    path('librarian/reject/<int:pk>/',views.reject_request_api,name='reject_request_api'),
]