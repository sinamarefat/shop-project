from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)
        
        if not user.is_verified:
            raise ValidationError("user is not verified")



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email",)

    # اگر می‌خواهی فیلدها استایل بوت‌استرپ بگیرند، این بخش را اضافه کن:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})