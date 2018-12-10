from django.contrib.auth.views import LoginView
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from user.forms import (
    ProfileForm, UserCreationFormCustom, UpdateUserForm, PasswordForm)
from user.models import Profile
from django.contrib.auth.decorators import login_required


class CustomLoginView(LoginView):
    @receiver(user_logged_in)
    def logged_in(sender, user, request, **kwargs):
        print(f'User: {user} has logged in')


def update_user_and_profile(user_form, profile_form):
    user = user_form.save()
    # load the profile instance created by the signal
    user.refresh_from_db
    user.profile.id_card = profile_form.cleaned_data['id_card']
    user.profile.phone_number = \
        profile_form.cleaned_data['phone_number']
    user.profile.gender = profile_form.cleaned_data['gender']
    user.profile.birth_date = \
        profile_form.cleaned_data['birth_date']
    user.save()


@transaction.atomic
def registrationFormExtended(request):
    register_url = 'user/register.html'
    if request.method == 'POST':
        user_form = UserCreationFormCustom(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            update_user_and_profile(user_form, profile_form)
            return redirect(to='user:login')
        return render(request, register_url, context={
            'user_form': user_form,
            'profile_form': profile_form
        })
    return render(request, register_url, context={
        'user_form': UserCreationFormCustom(),
        'profile_form': ProfileForm(),
    })


@login_required
@transaction.atomic
def edit_user_info(request):
    register_url = 'user/edit_user.html'
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        password_form = PasswordForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid() and \
                password_form.is_valid():
            if check_password(password_form.cleaned_data['password'],
                              request.user.password):
                update_user_and_profile(user_form, profile_form)
                msg = 'Info successfully updated'
                msg_type = 'SUCCESS'
            else:
                print('password does not match')
                msg = 'Password is incorrect'
                msg_type = 'ERROR'
        return render(request, register_url, context={
            'user_form': user_form,
            'profile_form': profile_form,
            'msg_type': msg_type,
            'password_form': PasswordForm(),
            'msg': msg
        })

    return render(request, register_url, context={
        'user_form': UpdateUserForm(instance=request.user),
        'profile_form': ProfileForm(instance=profile),
        'password_form': PasswordForm()
    })
