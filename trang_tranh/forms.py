from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={"placeholder": "Username"}))
    password1 = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password confirmation"}))

    email = forms.EmailField(
        max_length=254,
        help_text="Required. Inform a valid email address.",
        widget=TextInput(attrs={"placeholder": "Email"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=PasswordInput(attrs={"placeholder": "Password"}))
