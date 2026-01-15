from django import forms
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label

User = get_user_model()

class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label="Status"
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Executor"
    )
    label = forms.ModelChoiceField(
    queryset=Label.objects.all(),
    required=False,
    label="Label",
    widget=forms.Select(attrs={
        "class": "form-select mr-3 ml-2"
    })
)
    own_tasks = forms.BooleanField(
        required=False,
        label="Only your tasks"
    )



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
        widgets = {
            "label": forms.Select(
                attrs={
                    "size": 8,
                    "style": "width: 100%;"
                }
            ),
         }
