from django.contrib.auth.views import LoginView
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from django.shortcuts import render
from django.shortcuts import redirect
from user.forms import ProfileForm, UserCreationFormCustom


class CustomLoginView(LoginView):
    @receiver(user_logged_in)
    def logged_in(sender, user, request, **kwargs):
        print(f'User: {user} has logged in')


@transaction.atomic
def registrationFormExtended(request):
    register_url = 'user/register_extended.html'
    if request.method == 'POST':
        user_form = UserCreationFormCustom(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # load the profile instance created by the signal
            user.refresh_from_db()

            user.profile.id_card = profile_form.cleaned_data['id_card']
            user.profile.phone_number = \
                profile_form.cleaned_data['phone_number']
            user.profile.gender = profile_form.cleaned_data['gender']
            user.profile.date_of_birth = \
                profile_form.cleaned_data['date_of_birth']
            user.save()
            return redirect(to='user:login')
        return render(request, register_url, context={
            'user_form': user_form,
            'profile_form': profile_form
        })
    return render(request, register_url, context={
        'user_form': UserCreationFormCustom(),
        'profile_form': ProfileForm(),
    })
