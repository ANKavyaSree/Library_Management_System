from django.urls import path
from . import views
urlpatterns = [
    path('my-fines/',views.my_fines,name='my_fines'),
    path('pay/<int:fine_id>/',views.pay_fine,name='pay_fine'),
    # ======================================
    # USER APIs
    # ======================================
    path('fines/my-fines/',views.my_fines_api,name='my_fines_api'),
    path('fines/unpaid/',views.unpaid_fines_api,name='unpaid_fines_api'),
    path('fines/pay/<int:pk>/',views.pay_fine_api,name='pay_fine_api'),
    # ======================================
    # LIBRARIAN APIs
    # ======================================
    path('librarian/all-fines/',views.all_fines_api,name='all_fines_api'),
    path('librarian/add-fine/',views.add_fine_api,name='add_fine_api'),
]