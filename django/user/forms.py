from django import forms
from django.contrib.auth import get_user_model
from user.models import Profile


class BankRegisterForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True
    )

    gender = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=Profile.GENDERS
    )

    date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name',
                  'id_card', 'phone_number', 'date_of_birth']
