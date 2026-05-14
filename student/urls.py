from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='student_dashboard'),
    path('my-requests/',views.my_requests,name='student_requests'),
]