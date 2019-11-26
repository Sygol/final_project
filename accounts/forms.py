from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from accounts.models import CustomUser


class CustomUserSignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['class'] = 'form-control'

    username = forms.CharField(label='Username', max_length=32, widget=forms.TextInput(
        attrs={'placeholder': "Enter username"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'placeholder': "Enter email"}))
    first_name = forms.CharField(label='First name', max_length=32, widget=forms.TextInput(
        attrs={'placeholder': "Enter first name"}))
    last_name = forms.CharField(label='Last name', max_length=32, widget=forms.TextInput(
        attrs={'placeholder': "Enter last name"}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': "Enter password"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'placeholder': "Confirm password"}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name']
