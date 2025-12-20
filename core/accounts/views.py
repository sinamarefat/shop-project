from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegistrationForm # فرمی که قبلاً ساختیم
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationForm

class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    
    
class LogoutView(auth_views.LogoutView):
    pass


from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from .forms import RegistrationForm # فرمی که قبلاً ساختیم

class SignupView(SuccessMessageMixin, generic.CreateView):
    form_class = RegistrationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')
    success_message = "ثبت‌نام شما با موفقیت انجام شد. پس از تایید مدیریت می‌توانید وارد شوید."

    def form_valid(self, form):
        # اینجا می‌توانید قبل از ذخیره نهایی، تغییراتی روی کاربر اعمال کنید
        return super().form_valid(form)