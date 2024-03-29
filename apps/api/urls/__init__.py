from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path(
        "obtain/token/",
        include("apps.api.urls.obtain_token"),
    ),
    path(
        "tasks/",
        include("apps.api.urls.tasks"),
    ),
    path(
        "manage/task/",
        include("apps.api.urls.manage_task_state"),
    ),
]
