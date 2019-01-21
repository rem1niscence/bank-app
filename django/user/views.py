from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.conf import settings
from user.forms import (
    ProfileForm, UserCreationFormCustom, UpdateUserForm, PasswordForm)

#para utilizar el servicio de mensajeria luego de que el usuario se registra (email de confirmacion de registro)
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

#para mandar los datos del cliente en el email
from core.apis import id_card_exists, get_client, get_accounts, get_account_movements

"""
Las funciones que trataremos en esta vista son:
1. registrationFormExtended
2. activate
3. edit_user_info
"""

@transaction.atomic
def registrationFormExtended(request):
    if request.method == 'POST':
        user_form = UserCreationFormCustom(request.POST) #formulario para el modelo de usuario
        profile_form = ProfileForm(request.POST)        #formulario para el modelo de PROFILE
        if user_form.is_valid() and profile_form.is_valid(): #Comprueba si la info del form es valida

            user = user_form.save(commit=False)
            user.is_active = False #parte del email system. Mantiene al usuario inhabilitado hasta que se acceda al link de confirmacion de
            user.save()             #usuario enviado por email. Si intenta logearse, no tendra acceso.
            
            profile = profile_form.save(user)
            profile.core_id = profile_form.core_id
            profile.save()
            #parte del email system
            
            #primero conseguiremos la informacion del cliente que enviaremos a traves del email
            cedula = profile_form.cleaned_data.get('id_card')
            cedula_json = id_card_exists(cedula)
            id_cliente = cedula_json['mensaje']
            cliente_json = get_client(id_cliente)

            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta de Internet Banking'
            message = render_to_string('acc_active_email.html', {
                'datos_cliente': cliente_json,
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/ConfirmarEmail.html')
            #return redirect(to=settings.LOGIN_URL)
    else:
        user_form = UserCreationFormCustom()
        profile_form = ProfileForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'user/register.html', context=context)

#para el email system
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'user/LinkConfirmacion.html')
    else:
        return HttpResponse('Activation link is invalid!')


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
