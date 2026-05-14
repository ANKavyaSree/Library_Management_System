from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',views.dashboard,name='teacher_dashboard'),
    path('my-requests/',views.my_requests,name='teacher_requests'),
]