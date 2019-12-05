from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from accounts.models import CustomUser
from money_tracker.models import Currency


class CustomUserSignUpForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'currency', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in ['username', 'email', 'password1', 'password2', 'currency']:
            self.fields[fieldname].help_text = None
            self.fields[fieldname].widget.attrs['class'] = 'form-control'
        self.fields["currency"].choices = [("", "Choose currency"), ] + list(self.fields["currency"].choices)[1:]

    username = forms.CharField(label='Username', max_length=32, widget=forms.TextInput(
        attrs={'placeholder': "Enter username"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={'placeholder': "Enter email"}))
    currency = forms.ModelChoiceField(label='Currency', queryset=Currency.objects.all())
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': "Enter password"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'placeholder': "Confirm password"}))


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['username', 'currency', 'email']
