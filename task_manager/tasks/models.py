from django.db import models
from django.contrib.auth import get_user_model
from task_manager.statuses.models import Status
from django.utils.translation import gettext_lazy as _
from task_manager.labels.models import Label

User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name=_("Name")
    )
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name=_("Status")
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="executed_tasks",
        verbose_name=_("Executor")
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="authored_tasks",
        verbose_name=_("Author")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )

    labels = models.ManyToManyField(
        'labels.Label',
        blank=True,
        related_name="tasks",
        verbose_name=_("Labels")
    )

    class Meta:
        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
