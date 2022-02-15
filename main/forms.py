from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, TextInput

from .models import Profile, ProfileImage


class UserRegistrationForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileUpdateImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']


class ProfileUpdatePNumberForm(forms.ModelForm):
    phone_number = forms.CharField(label='Номер телефона', max_length=20)

    class Meta:
        model = Profile
        fields = ['phone_number']
