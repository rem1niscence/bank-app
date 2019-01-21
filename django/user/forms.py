from django import forms
from django.contrib.auth import get_user_model
from user.models import Profile
from django.contrib.auth.forms import UserCreationForm
from core.apis import id_card_exists


class UserCreationFormCustom(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField(max_length=200, help_text='Required')

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

    class Meta:
        model = Profile
        # fields = ('id_card', 'gender', 'birth_date', 'phone_number')
        fields = ('id_card',)

    def save(self, user, commit=True):
        profile_form = super(ProfileForm, self).save(commit=False)
        profile = Profile.objects.get(pk=user.id)

        profile.id_card = profile_form.id_card
 
        if commit:
            profile.save()
        return profile

    def is_valid(self):
        valid = super(ProfileForm, self).is_valid()
        if not valid:
            return valid

        # Check if user exist on the database
        check_id_card = id_card_exists(self.cleaned_data['id_card'])
        if check_id_card['exito']:
            self.core_id = check_id_card['mensaje']
            return valid
        else:
            self.add_error('id_card', check_id_card['mensaje'])
            return False


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
