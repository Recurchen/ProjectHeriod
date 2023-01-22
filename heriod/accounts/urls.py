from cProfile import Profile
from django.urls import path

from .views import SignUpView, LoginView, LogoutView, ProfileView, ProfileEditView

app_name = 'accounts'

urlpatterns = [
    
    path('signup/',SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView),
    
    
    path('profile/view/', ProfileView, name = "profile_view"),
    path('profile/edit/', ProfileEditView.as_view()),
]
