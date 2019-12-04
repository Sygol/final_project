from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin

from accounts.forms import CustomUserSignUpForm, CustomUserChangeForm
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserSignUpForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'username', 'email', 'created', 'modified']
    exclude = ('modified',)
