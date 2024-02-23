from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import TasksSerializer
from apps.api.validators import ManageTaskStateValidate
from apps.task_system.service import ServiceTasks


class ManageTaskStateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TasksSerializer
    validations_class = ManageTaskStateValidate
    service_class = ServiceTasks

    def post(self, request, pk: int) -> Response:
        get_validation = self.validations_class(request.data)
        if get_validation.validate():
            try:
                _queryset = self.service_class(pk, **get_validation.data).execute()
            except Exception as e:
                return Response(
                    {"message_error": str(e)}, status=status.HTTP_400_BAD_REQUEST
                )

            return Response(
                {
                    "message_success": "Status was updated success",
                    "data": self.serializer_class(_queryset).data,
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(get_validation.errors(), status=status.HTTP_400_BAD_REQUEST)
