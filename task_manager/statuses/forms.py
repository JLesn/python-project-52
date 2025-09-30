from django import forms
from .models import Status
from django.utils.translation import gettext_lazy as _


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ("name",)
        labels = {
            "name": _("Name"),
        }
        
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if Status.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(_('A status with this name already exists.'))
        return name


