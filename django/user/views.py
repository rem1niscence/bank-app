from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from user.forms import (
    ProfileForm, UserCreationFormCustom, UpdateUserForm, PasswordForm)


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
    if request.method == 'POST':
        user_form = UserCreationFormCustom(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            update_user_and_profile(user_form, profile_form)
            return redirect(to='user:login')
    else:
        user_form = UserCreationFormCustom()
        profile_form = ProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user/register.html', context=context)


@login_required
@transaction.atomic
def edit_user_info(request):
    msg = None
    msg_type = None
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        password_form = PasswordForm(request.POST)

        forms_valid = user_form.is_valid() and profile_form.is_valid() and \
            password_form.is_valid()
        if forms_valid:
            password_match = check_password(
                password_form.cleaned_data['password'], request.user.password)
            if password_match:
                update_user_and_profile(user_form, profile_form)
                msg = 'Changes successfully saved'
                msg_type = 'SUCCESS'
            else:
                msg = 'Password is incorrect'
                msg_type = 'ERROR'
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        password_form = PasswordForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'msg': msg,
        'msg_type': msg_type,
    }

    return render(request, 'user/edit_user.html', context=context)
