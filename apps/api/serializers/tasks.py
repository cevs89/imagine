from rest_framework import serializers

from apps.task_system.models import TasksModels


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = TasksModels
        fields = [
            "id",
            "name",
            "description",
            "status",
            "uuid",
            "is_active",
            "created_at",
            "modified_at",
        ]
