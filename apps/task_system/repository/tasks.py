from django.db import IntegrityError, transaction
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from apps.task_system.models import TasksModels


class RepositoryTasks:
    def __init__(self) -> None:
        self.model = TasksModels

    @property
    def get_queryset_all(self) -> QuerySet[TasksModels]:
        return self.model.objects.filter(is_active=True)

    def get_queryset(self, _id: id) -> TasksModels:
        try:
            queryset = self.model.objects.get(pk=_id)
        except self.model.DoesNotExist:
            raise ValueError(_("Task Doesn't exists")) from None

        return queryset

    def update_status(self, _id: id, _status: str) -> TasksModels:
        _queryset = self.get_queryset(_id)
        try:
            with transaction.atomic():
                _queryset.status = _status
                _queryset.save()
        except (Exception, IntegrityError) as e:
            raise ValueError(str(e)) from e

        return _queryset
