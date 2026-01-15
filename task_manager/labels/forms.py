from django import forms
from .models import Label
from django.utils.translation import gettext_lazy as _


class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ("name",)
        labels = {
            "name": _("Name"),
        }
        
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        qs = Label.objects.filter(name__iexact=name)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)  # ← исключаем текущую метку
        if qs.exists():
            raise forms.ValidationError(_('A label with this name already exists.'))
        return name