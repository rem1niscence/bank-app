from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.conf import settings
from user.forms import (
    ProfileForm, UserCreationFormCustom, UpdateUserForm, PasswordForm)


@transaction.atomic
def registrationFormExtended(request):
    if request.method == 'POST':
        user_form = UserCreationFormCustom(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            profile = profile_form.save(user)
            profile.core_id = profile_form.core_id
            profile.save()
            return redirect(to=settings.LOGIN_URL)
    else:
        user_form = UserCreationFormCustom()
        profile_form = ProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/register.html', context=context)


@login_required
@transaction.atomic
def edit_user_info(request):
    msg = None
    msg_type = None
    user = request.user
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            password_match = check_password(
                request.POST['password'], user.password)
            if password_match:
                user = user_form.save()
                profile_form.save(user)
                msg = 'Changes successfully saved'
                msg_type = 'SUCCESS'
            else:
                msg = 'Password is incorrect'
                msg_type = 'ERROR'
    else:
        user_form = UpdateUserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': PasswordForm(),
        'msg': msg,
        'msg_type': msg_type,
    }

    return render(request, 'user/edit_user.html', context=context)
