from django.urls import path
from . import views
urlpatterns = [
    path('my-fines/',views.my_fines,name='my_fines'),
    path('pay/<int:fine_id>/',views.pay_fine,name='pay_fine'),
]