from django import forms
from django.contrib.auth import get_user_model
from user.models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext, gettext_lazy as _


class UserCreationFormCustom(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name',
                  'email')

    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    """
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}))

    phone_number = forms.CharField(label='Numero de telefono', error_messages={
        'nomatch': 'Must be a 10 digits dominican number'
    }, max_length=10)
    """

    class Meta:
        model = Profile
        #fields = ('id_card', 'gender', 'birth_date', 'phone_number')
        fields = ('id_card',)

    def save(self, user, commit=True):
        profile_form = super(ProfileForm, self).save(commit=False)
        profile = Profile.objects.get(pk=user.id)

        profile.id_card = profile_form.id_card
        """
        profile.phone_number = profile_form.phone_number
        profile.gender = profile_form.gender
        profile.birth_date = profile_form.birth_date
        """
        if commit:
            profile.save()
        return profile

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
