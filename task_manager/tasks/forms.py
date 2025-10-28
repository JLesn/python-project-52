from django import forms
from .models import Task
from task_manager.statuses.models import Status
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

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
    label = forms.CharField(
        required=False,
        label="Label"
    )
    own_tasks = forms.BooleanField(
        required=False,
        label="Only your tasks"
    )



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ("name", "description", "status", "executor", "labels")
        labels = {
            "name": _("Name"),
            "description": _("Description"),
            "status": _("Status"),
            "executor":_("Executor"),
        }
        
