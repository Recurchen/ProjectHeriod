from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError


# Task 1
class SignUpForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(required=False)
    age = forms.IntegerField()

    def clean(self):
        data = super().clean()

        if len(data.get('username')) == 0:
            self.add_error('username', 'This field is required')
        if len(data.get('password1')) == 0:
            self.add_error('password1', 'This field is required')
        if len(data.get('password2')) == 0:
            self.add_error('password2', 'This field is required')

        if len(data.get('password1')) < 8:
            self.add_error('password1', 'This password is too short. It must contain at least 8 characters')
        if data.get('password1') != data.get('password2'):
            self.add_error('password2', "The two password fields didn't match")
        if User.objects.filter(username=data.get('username')).exists():
            self.add_error('username', 'A user with that username already exists')

        if len(data.get('email')) > 0:
            try:
                validate_email(data.get('email'))
            except ValidationError:
                self.add_error('email', 'Enter a valid email address')

        return data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        data = super().clean()

        if not (user := authenticate(username=data.get('username'), password=data.get('password'))):
            self.add_error('password', 'Username or password is invalid')

        data["user"] = user

        return data


# Task 2
class EditForm(UserChangeForm):
    password = None
    password1 = forms.CharField(required = False, widget=forms.PasswordInput)
    password2 = forms.CharField(required = False, widget=forms.PasswordInput)
    age = forms.IntegerField(required = False, min_value= 1)

    class Meta:
        model = User
        fields = ("email",)

    def clean(self):
        data = super().clean()

        if data.get('password1') != data.get('password2'):
            self.add_error('password2', "The two password fields didn't match")
        if len(data.get('password1')) > 0 and len(data.get('password1')) < 8:
            self.add_error('password1', "This password is too short. It must contain at least 8 characters")

        if len(data.get('email')) > 0:
            try:
                validate_email(data.get('email'))
            except ValidationError:
                self.add_error('email', "Enter a valid email address")

        return data