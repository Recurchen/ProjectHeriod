from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from accounts.forms.forms import SignUpForm, LoginForm, EditForm
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash

from .models import AppUser

# Create your views here.

class SignUpView(FormView):
    template_name = 'form.html'
    form_class = SignUpForm

    def form_valid(self, form):
        new_user = User.objects.create_user(
            username = form.cleaned_data["username"],
            password = form.cleaned_data["password1"],
            email =  form.cleaned_data["email"],
        )
        AppUser.objects.create(
            user = new_user,
            age=form.cleaned_data["age"],
            )
        return HttpResponseRedirect(f"/accounts/login/")
        
class LoginView(FormView):
    template_name = 'form.html'
    form_class = LoginForm

    def form_valid(self, form):
        login(self.request, form.cleaned_data['user'])
        return HttpResponseRedirect(f"/accounts/profile/view/")

def LogoutView(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            logout(request)
    return HttpResponseRedirect(f"/accounts/login/")

# task 2
def ProfileView(request):
    if request.method == "GET":
        if request.user.is_authenticated:

            appuser = AppUser.objects.get(user=request.user)
            
            return JsonResponse({"id": request.user.id, 
                                "username": request.user.username,
                                "email": request.user.email,
                                "age": appuser.age
                                })
        else:
            return HttpResponse(status=401)

class ProfileEditView(generic.UpdateView):
    form_class = EditForm
    template_name = 'form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        user = form.save()
        if(len(form.cleaned_data['password1']) > 0):
            user.set_password(form.cleaned_data['password2'])
            update_session_auth_hash(self.request, self.request.user)
            user.save()
        return HttpResponseRedirect(f"/accounts/profile/view/")
    
