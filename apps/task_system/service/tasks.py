from django.utils.translation import gettext_lazy as _

from apps.task_system.models import TasksModels
from apps.task_system.repository import RepositoryTasks


class ServiceTasks:
    def __init__(self, _id: int, status: str) -> None:
        self.model = TasksModels
        self.repository = RepositoryTasks()
        self.id: int = _id
        self.status: str = status

    def _change_task_state(self):
        return self.repository.update_status(self.id, self.status)

    def _validate_current_task_state(self) -> None:
        _queryset = self.repository.get_queryset(self.id)
        if _queryset.status == self.status:
            raise ValueError(
                _(
                    f"Current status for tasks {_queryset.name} is {self.status} the same that you try to update."
                )
            )

    def execute(self):
        try:
            self._validate_current_task_state()
        except Exception as e:
            raise ValueError(str(e)) from e

        try:
            _update = self._change_task_state()
        except Exception as e:
            raise ValueError(str(e)) from e

        return _update
