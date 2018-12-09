from django import forms
from django.contrib.auth import get_user_model
from user.models import Profile


class ProfileForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        widget=forms.HiddenInput,
        queryset=get_user_model().objects.all(),
        disabled=True
    )

    date_of_birth = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Profile
        fields = '__all__'
