from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),
    path(
    'check-session/',
    views.check_session,
    name='check_session'
),

    #API URLS
    path('api/register/',views.register_api),
    path('api/login/',views.login_api),
    path('api/profile/',views.profile_api),
    path('api/logout/',views.logout_api)
]