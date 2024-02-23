from django.db import models

from apps.core.models import BaseModel
from apps.task_system.helpers.enums_tasks_state import ENUMS_TASK_STATE_MAP


class TasksModels(BaseModel):
    """
    Field: status
        For this purpose, we are going to set the status field with the possible values,
        these values are in the task document. Probably, for another purpose we will need to change
        the status field by a relationship to another database table. But for our purpose this is fine.

    Field: name
        Probably, the name field could be unique with a differentiator, example unique per user,
        but for this purpose it will only be globally unique
    """

    name = models.CharField(max_length=150, null=False, unique=True)
    description = models.TextField()
    status = models.CharField(choices=ENUMS_TASK_STATE_MAP, max_length=8, default="NEW")

    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.name
