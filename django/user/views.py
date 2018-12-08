from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from user.forms import BankRegisterForm


class ExampleRegisterView(CreateView):
    form_class = BankRegisterForm
    template_name = 'user/register_extended.html'

    def get_initial(self):
        return {'user': self.request.user.id}


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('core:home')


class CustomLoginView(LoginView):
    @receiver(user_logged_in)
    def logged_in(sender, user, request, **kwargs):
        print(f'User: {user} has logged in')
