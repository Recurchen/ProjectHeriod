from cProfile import Profile
from django.urls import path

from .views import (
    # task 3
    NewRecordView,
    SuccessAdd
)

app_name = 'records'

urlpatterns = [    

    path('add/', NewRecordView.as_view(), name = 'add_record'),
    path('successfuladd/', SuccessAdd, name='success_add'),
    
]
