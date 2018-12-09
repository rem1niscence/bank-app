from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from user.forms import ProfileForm
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest


class CustomLoginView(LoginView):
    @receiver(user_logged_in)
    def logged_in(sender, user, request, **kwargs):
        print(f'User: {user} has logged in')


@transaction.atomic
def registrationFormExtended(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            created_user = user_form.save()
            profile_form = ProfileForm(
                request.POST, initial={'user': created_user.id})
            if profile_form.is_valid():
                profile_form.save()
                return redirect(to='core:home')
        return HttpResponseBadRequest()
    else:
        ctx = {
            'user_form': UserCreationForm(),
            'profile_form': ProfileForm(),
        }
    return render(request, 'user/register_extended.html', context=ctx)
