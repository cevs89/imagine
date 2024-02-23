from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.api.serializers import TasksSerializer
from apps.task_system.models import TasksModels


class TasksViewSet(viewsets.ModelViewSet):
    queryset = TasksModels.objects.all()
    serializer_class = TasksSerializer
    permission_classes = [IsAuthenticated]
