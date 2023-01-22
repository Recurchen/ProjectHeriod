from cProfile import Profile
from django.urls import path

from .views import (
    # task 3
    EstimateView,
    NewRecordView,
)

app_name = 'records'

urlpatterns = [    

    path('add/', NewRecordView.as_view(), name = 'add_record'),
    path('estimate/', EstimateView, name='success_add'),
    
]
