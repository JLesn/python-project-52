from django import forms
from django.utils.translation import gettext_lazy as _
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2')
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'username': _('Username'),
            'password1': _('Password'),
            'password2': _('Password confirmation'),
        }
        help_texts = {
            'password1': _('Enter a secure password. Minimum 8 characters.'),
            'password2': _('Repeat the password for confirmation.'),
        }


class CustomUserChangeForm(forms.ModelForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        required=False,
        strip=False,
        widget=forms.PasswordInput(
            render_value=False,
            attrs={
                "autocomplete": "new-password",
                "readonly": "readonly",
                "onfocus": "this.removeAttribute('readonly')",
            }
        ),
        help_text=_("Leave empty if you do not want to change the password."),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name', 'username')
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'username': _('Username'),
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError(_("Passwords do not match"))
            if len(password1) < 8:
                raise forms.ValidationError(_("Password must be at least 8 characters long"))

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get("new_password1")
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('username', 'password')