from django.urls import path
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    #API URLS
    path('api/register/', views.register_api),
    path('api/login/', views.login_api),
    path('api/logout/', views.logout_api),
]