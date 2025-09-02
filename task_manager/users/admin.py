from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import MyUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = MyUser
    list_display = ['first_name', 'last_name', 'username',]

admin.site.register(MyUser, CustomUserAdmin)
