from django.urls import path

from apps.api.views import ManageTaskStateView

urlpatterns = [
    path("state/<int:pk>/", ManageTaskStateView.as_view(), name="manage_task_state"),
]
