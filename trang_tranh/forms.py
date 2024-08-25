from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.utils.translation import gettext_lazy as _
from .models import WRITING_MODE



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

# Create custom file file for multiple uploads
class MultipleImageInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleImageInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_image_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_image_clean(d, initial) for d in data]
        else:
            result = single_image_clean(data, initial)
        return result

class PostForm(forms.Form):
    text_content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': _("What's on your mind?"), 'dir': "auto", "rows": "1"}), max_length=500, required=True)
    writing_mode = forms.ChoiceField(choices=WRITING_MODE)
    media = MultipleImageField(required=False)